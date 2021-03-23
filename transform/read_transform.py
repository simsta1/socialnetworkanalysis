import pandas as pd
import numpy as np


def transform(df):
    """
    (pd.DataFrame) --> pd.DataFrame

    Transforms the Tweets Data.

    @param df: pd.DataFrame(), which shall be transformed
    @return: pd.DataFrame()

    """
    # Drop Unnamed columns
    drop_cols = [col for col in df.columns if 'Unnamed' in col]
    df = df.drop(drop_cols, axis=1)

    # Set pd datetime of date
    df['creation_date'] = pd.to_datetime(df['creation_date'])
    df['profile_created_at'] = pd.to_datetime(df['profile_created_at'])

    # If start of the Twitter post with RT then set to true
    # Add new column if it is retweet
    df['is_retweet'] = df['full_text'].str.contains(pat=r'^RT', regex=True)

    # Change the format of column mentions to a list
    df['mentions'] = np.where(df['mentions'] == '[]', np.nan, df['mentions'])
    df['mentions'] = df['mentions'].str.strip('[]').str.split(',')

    # Change the column hashtags to nan when empty else to a list
    df['entities_hashtags'] = np.where(df['entities_hashtags'] == '[]', np.nan, df['entities_hashtags'])
    df['entities_hashtags'] = df['entities_hashtags'].str.findall(pat=r"'(\w+)'")

    return df


def read_transform(path_tweets, path_retweets, join_method='concat'):
    """
    (str) --> pd.DataFrame()

    This function reads data from the two dataframes tweet and retweets.

    @param path_tweets: specify path of tweets csv file to read
    @param path_retweets: specify path of retweets csv to read
    @param join_method: 'concat' or 'join'
    if concat: then dataframe gets concateanted over axis=0
    if join then dataframe will be left joined together
    @return: pandas dataframe

    """
    # Read Dataframes of Tweets and Retweets
    tweets = pd.read_csv(path_tweets)
    retweets = pd.read_csv(path_retweets)

    tweets = transform(df=tweets)
    retweets = transform(df=retweets)

    if join_method == 'concat':
        data = pd.concat([tweets, retweets],
                         axis=0
                         )
    elif join_method == 'join':
        data = pd.merge(left=tweets, right=retweets,
                        left_on='tweet_id', right_on='RT_of_ID',
                        how='left'
                        )

    return data