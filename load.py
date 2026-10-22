
import os
import json
import logging
import psycopg2
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def read_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def load_data():
    connection = None

    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "api_analytics_db"),
            user=os.getenv("DB_USER", "pipeline_user"),
            password=os.getenv("DB_PASSWORD")
        )

        cursor = connection.cursor()

        # Load users first because posts reference users
        users = read_json("data/clean_users.json")

        for user in users:
            cursor.execute(
                """
                INSERT INTO users
                    (id, name, username, email, city, company_name)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    username = EXCLUDED.username,
                    email = EXCLUDED.email,
                    city = EXCLUDED.city,
                    company_name = EXCLUDED.company_name
                """,
                (
                    user["id"],
                    user["name"],
                    user["username"],
                    user["email"],
                    user.get("city"),
                    user.get("company_name")
                )
            )

        # Load posts after users
        posts = read_json("data/clean_posts.json")

        for post in posts:
            cursor.execute(
                """
                INSERT INTO posts (id, user_id, title, body)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    user_id = EXCLUDED.user_id,
                    title = EXCLUDED.title,
                    body = EXCLUDED.body
                """,
                (
                    post["id"],
                    post["user_id"],
                    post["title"],
                    post.get("body")
                )
            )

        # Load comments after posts
        comments = read_json("data/clean_comments.json")

        for comment in comments:
            cursor.execute(
                """
                INSERT INTO comments
                    (id, post_id, name, email, body)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    post_id = EXCLUDED.post_id,
                    name = EXCLUDED.name,
                    email = EXCLUDED.email,
                    body = EXCLUDED.body
                """,
                (
                    comment["id"],
                    comment["post_id"],
                    comment.get("name"),
                    comment.get("email"),
                    comment["body"]
                )
            )

        # Commit all changes together
        connection.commit()

        print(f"Users loaded: {len(users)}")
        print(f"Posts loaded: {len(posts)}")
        print(f"Comments loaded: {len(comments)}")
        print("Data loaded successfully!")

        logging.info("Database load completed successfully.")

    except Exception as error:
        if connection:
            connection.rollback()

        logging.exception("Database load failed.")
        print(f"Loading failed: {error}")

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    load_data()
