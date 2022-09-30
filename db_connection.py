import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists


def get_conn() -> sqlalchemy.engine.base.Engine:
    """
    Creates a database connection with the given URL

    @output: sqlalchemy.engine.base.Engine
    """
    url = 'postgresql://gio:docker@localhost:5433/ted_talks'

    if not database_exists(url):
        create_database(url)
        engine = create_engine(url)
    else:
        engine = create_engine(url)

    return engine
