
import json
import logging
import pandas as pd

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_json(filename):
    """Load records from a JSON file."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def clean_text(value):
    """Remove unnecessary spaces from text."""
    if isinstance(value, str):
        return value.strip()
    return value


def save_clean_data(df, filename):
    """Save cleaned records as JSON."""
    df.to_json(
        filename,
        orient="records",
        indent=4,
        force_ascii=False
    )


def main():
    # 1. Load the raw data
    users = pd.json_normalize(load_json("data/users.json"))
    posts = pd.json_normalize(load_json("data/posts.json"))
    comments = pd.json_normalize(load_json("data/comments.json"))

    print("Raw record counts:")
    print("Users:", len(users))
    print("Posts:", len(posts))
    print("Comments:", len(comments))

    # 2. Select and flatten the columns we need
    users = users[
        ["id", "name", "username", "email",
         "address.city", "company.name"]
    ].rename(columns={
        "address.city": "city",
        "company.name": "company_name"
    })

    posts = posts[["id", "userId", "title", "body"]].rename(
        columns={"userId": "user_id"}
    )

    comments = comments[
        ["id", "postId", "name", "email", "body"]
    ].rename(columns={"postId": "post_id"})

    # 3. Clean text fields
    for df in [users, posts, comments]:
        for column in df.select_dtypes(include="object").columns:
            df[column] = df[column].map(clean_text)

    # 4. Remove duplicate IDs
    users = users.drop_duplicates(subset=["id"])
    posts = posts.drop_duplicates(subset=["id"])
    comments = comments.drop_duplicates(subset=["id"])

    # 5. Remove records with missing required fields
    users = users.dropna(
        subset=["id", "name", "username", "email"]
    )
    posts = posts.dropna(
        subset=["id", "user_id", "title"]
    )
    comments = comments.dropna(
        subset=["id", "post_id", "email", "body"]
    )

    # 6. Validate relationships between tables
    valid_user_ids = set(users["id"])
    valid_post_ids = set(posts["id"])

    posts = posts[posts["user_id"].isin(valid_user_ids)]
    comments = comments[comments["post_id"].isin(valid_post_ids)]

    # 7. Save the cleaned data
    save_clean_data(users, "data/clean_users.json")
    save_clean_data(posts, "data/clean_posts.json")
    save_clean_data(comments, "data/clean_comments.json")

    # 8. Print the results
    print("\nCleaned record counts:")
    print("Users:", len(users))
    print("Posts:", len(posts))
    print("Comments:", len(comments))

    print("\nCleaning completed successfully!")

    logging.info(
        "Cleaning completed. Users=%s, Posts=%s, Comments=%s",
        len(users), len(posts), len(comments)
    )


if __name__ == "__main__":
    main()
