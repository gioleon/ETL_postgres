"""
Let's do some of feature engineering.
"""
import re
import datetime
import numpy as np
import pandas as pd
from pathlib import Path
from db_operations import ingest_data

pd.options.mode.chained_assignment = None

# Root path
root_path = Path(__file__).parent


def map_likes(like: str) -> int:
    """
    Replaces M of million for the corresponding zeros
    and K for 000

    @input: like(str)

    @output: like(int)
    """
    like = like.lower()
    like = like.replace('.', '')

    if like.endswith('m') and len(like) == 2:
        like = like.replace('m', '000000')
    elif like.endswith('m') and len(like) == 3:
        like = like.replace('m', '00000')
    else:
        like = like.replace('k', '000')

    return int(like)


def map_published_date(date: str) -> datetime.date:
    """
    Extracts date from format Y-D-MT_hour_Z to Y-M-D

    @input: date(str)

    @output: date(datetime.date)
    """
    date = date[0:10]
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    return date


def map_speakers_name(speaker: str) -> str:
    """
    Takes a str representation of a list, 
    then, extract from it the speaker's occupation.

    @input: speaker(str)
    @output: name(str)
    """
    # There is some records where we don't have name or occupation
    if len(speaker) != 2:

        # Find all elements inside ""
        name = re.findall('".+?"', speaker)

        """
        Delete elements into the list of elements inside "" 
        that are  equals to "name", "occupation" 
        """
        name = [
            n for n in name
            if n not in ['"name"', '"occupation"']
        ]

        """
        Transform from list to pandas.Series to use a list of 
        Index to select just names in the whole list
        """
        name = pd.Series(name).iloc[
            np.arange(0, len(name), 2)
        ]

        # Transform from pandas series to list
        name = name.values

        # Delete " from the elements
        name = list(map(lambda x: x.replace('"', ''), name))

        # Convert to string. We will use , as separator.
        name = ", ".join(name)

    else:
        return 'No name'

    return name


def map_speakers_occupation(speaker: str) -> str:
    """
    Takes a str representation of a list, 
    then, extract from it the speaker's occupation.

    @input: speaker(str)
    @output: occupation(str)
    """
    # There is some records where we don't have name or occupation
    if len(speaker) != 2:

        # Find all elements inside ""
        occupation = re.findall('".+?"', speaker)

        """
        Delete elements into the list of elements inside "" 
        that are  equals to "name", "occupation" 
        """
        occupation = [
            occ for occ in occupation
            if occ not in ['"name"', '"occupation"']
        ]

        """
        Transform from list to pandas.Series to use a list of 
        Index to select just occupations in the whole list
        """
        occupation = pd.Series(occupation).iloc[
            np.arange(1, len(occupation), 2)
        ]

        # Transform from pandas series to list
        occupation = occupation.values

        # Delete " from the elements
        occupation = list(map(lambda x: x.replace('"', ''), occupation))

        """
        Convert to string.

        As there are people with more than one occupation
        we will use ; as separator of people's occupation.
        """
        occupation = "; ".join(occupation)

    else:
        return 'no name'

    return occupation


def map_topics(topic: str) -> str:
    """
    Takes a list of dictionaries and 
    obtains from it the topic.
    """

    if len(topic) != 2:
        topics = re.findall('".+?"', topic)
        topics = [t for t in topics if t not in ['"id"', '"name"']]
        topics = pd.Series(topics).iloc[np.arange(1, len(topics), 2)].values
        topics = list(map(lambda x: x.replace('"', ''), topics))
        topics = ', '.join(topics)
    else:
        return 'no topic'

    return topics


def map_subtitle_languages(subtitle: str) -> str:
    """
    This function takes the list of dictionaries 
    with subtitles and returns only the name of the
    languages.
    """
    if len(subtitle) != 2:
        # Find all the characters inside ""
        subtitle = re.findall('".+?"', subtitle)

        # Delete the keys of the dictionaries from the list
        subtitle = [
            sub for sub in subtitle
            if sub not in ['"name"', '"code"']
        ]

        # Select just the name of the subtitles language
        subtitle = pd.Series(subtitle).iloc[
            np.arange(0, len(subtitle), 2)
        ].values

        # Remove "" from elements.
        subtitle = list(map(lambda x: x.replace('"', ''), subtitle))

        # Join the elements of the list to convert it to string
        subtitle = ', '.join(subtitle)

    else:
        return 'no subtitles'

    return subtitle


def load_data() -> pd.DataFrame:
    """
    This function loads the original 
    csv file.

    @output: pandas.DataFrame
    """
    # Path
    file_path = Path(
        root_path,
        "./data/preprocess/talks_info.csv"
    )

    # Read csv file
    df = pd.read_csv(file_path)

    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes the given dataframe and transforms it;
    then, returns a new DataFrame

    @input: pandas.DataFrame

    @output: pandas.DataFrame
    """

    # Delete "" from title
    df['title'] = list(map(lambda x: x.replace('"', ''), df['title']))

    # Convert likes column to only numbers
    df['likes'] = list(map(map_likes, df['likes'].values))

    # After taking a glance, i think duration column is in seconds,
    # then I'll convert it to minutes
    df['duration_min'] = list(map(
        lambda duration: duration/60,
        df['duration'].values)
    )

    # Transform published_date to a clearer format
    df['published_date'] = list(map(
        map_published_date,
        df['published_date'].values)
    )

    # Extract names from speakers
    df['speakers_name'] = list(map(
        map_speakers_name,
        df['speakers'].values)
    )

    # Extract occupations from speakers
    df['speakers_occupation'] = list(map(
        map_speakers_occupation,
        df['speakers'].values)
    )

    # Extract topics
    df['topics'] = list(map(map_topics, df['topics'].values))

    # Extract languages names from subtitles
    df['subtitle_languages'] = list(map(
        map_subtitle_languages,
        df['subtitle_languages'].values)
    )

    # Rename _id col
    df = df.rename({'_id': 'id'}, axis='columns')

    # Filter DataFrame by the columns of interest
    df = df[[
        'id', 'title',
        'duration_min', 'speakers_name',
        'speakers_occupation', 'event',
        'topics', 'views',
        'page_url', 'published_date',
        'recorded_date', 'subtitle_languages',
        'likes'
    ]]

    # Impute missing values
    df['speakers_occupation'] = df['speakers_occupation'].replace(
        '', 'no data')
    df['recorded_date'] = df['recorded_date'].replace(np.nan, 'no data')
    df['event'] = df['event'].replace(np.nan, 'no data')

    df.to_csv("./data/staging/cleaned_talks_info.csv", index=False)

    return df


def save_data_db(df: pd.DataFrame) -> None:
    """
    Calls a function that stores data into a table

    @input: pandas.DataFrame
    """

    # Store data
    ingest_data(df)


def main_transform():
    """
    Executes all function that belongs to its script
    """
    df = load_data()
    new_df = transform_data(df.copy())

    return new_df


main_transform()
