# API Data Engineering Pipeline

## Project Overview

This project demonstrates an end-to-end data engineering pipeline built with Python and PostgreSQL. It extracts data from REST APIs, cleans and validates the records, and loads the processed data into a relational database for analysis.

The pipeline is automated so that all stages can be executed with a single command.

## Architecture

REST APIs → Python Extraction → Data Cleaning and Validation → PostgreSQL → SQL Analytics

## Technologies Used

- **Python** — pipeline development and automation
- **REST APIs** — source data
- **Pandas** — data cleaning and transformation
- **PostgreSQL** — relational database storage
- **SQL** — joins, aggregations and analytical queries
- **Git and GitHub** — version control and project sharing

## Data Sources

The project uses the JSONPlaceholder API:

- Users
- Posts
- Comments

## Project Structure

```text
data-pipeline-project/
├── data/          # Generated data files (not committed)
├── logs/          # Pipeline logs
├── sql/           # SQL analytics queries
├── .env           # Local configuration (not committed)
├── .gitignore
├── extract.py
├── clean.py
├── load.py
├── pipeline.py
└── README.md
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/nnhandara/api-data-engineering-pipeline.git
cd data-pipeline-project
```

### 2. Install dependencies

Install the Python packages used by the project:

```bash
python3 -m pip install requests pandas python-dotenv psycopg2-binary
```

### 3. Configure environment variables

Create a local `.env` file with the required API URLs and PostgreSQL connection settings. Use your own database credentials and never commit this file.

### 4. Create the PostgreSQL database

Create the database, tables, and database user using the SQL definitions and setup instructions for this project.

### 5. Run the pipeline

```bash
python3 pipeline.py
```

The script runs extraction, cleaning, and loading in sequence, stopping when a stage fails.

## Data Validation and Loading

The pipeline cleans and validates API records before loading them into PostgreSQL. The loader uses conflict handling to support repeat runs without creating duplicate records for existing IDs.

## Example Analytics

The database supports analytical queries such as:

- Counting posts per user
- Ranking posts by number of comments
- Calculating comments per user
- Identifying users without posts

## Learning Objectives

This project demonstrates practical experience with API integration, data transformation, relational database design, SQL analytics, pipeline orchestration, logging, and version control.

## Future Improvements

- Add automated data quality tests
- Improve retry handling for API failures
- Schedule recurring pipeline runs
- Add Docker support
- Build a dashboard using Power BI

## Author

Data Science and Informatics graduate interested in data engineering, analytics, and building reliable data pipelines.
