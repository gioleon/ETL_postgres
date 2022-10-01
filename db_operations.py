import pandas as pd
from db_connection import get_conn

# Connection
engine = get_conn()


def ingest_data(df: pd.DataFrame) -> None:
    """
    Takes the given DataFrame end ingest its data 
    into a table.

    @input: pandas.DataFrame
    """
    df.to_sql('ted_talks', con=engine, if_exists='replace', index= False)


def create_table() -> None:
    """
    Takes the given sql query and creates a table.

    @input: string
    """
    sql = """
        CREATE TABLE IF NOT EXISTS ted_talks(
            _id INTEGER PRIMARY KEY,
            title VARCHAR(100), 
            duration_min FLOAT,
            speakers_name VARCHAR(260),
            speakers_occupation VARCHAR(480),
            event VARCHAR(50),
            topics VARCHAR(380),
            views INTEGER,
            page_url VARCHAR(160), 
            published_date VARCHAR(10),
            recorded_date VARCHAR(10),
            subtitle_languages VARCHAR(800),
            likes INTEGER
        );
    """

    engine.execute(sql)
