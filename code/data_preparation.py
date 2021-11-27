import pandas as pd
import numpy as np
from dateutil import parser
from datetime import date


def make_budget_genre_table(budgets_df, genres_df):
    """
    Joins tables containing budget and genre information by movie name and release date.
    Also turns release date info into a datetime and drops 'original_title', 'runtime_minutes' columns

    Arg:
        budgets_df (pdDataFrame): df containing information about budgets with "movie" and "release date" columns containing strings
        genres_df (pdDataFrame): df containing information about genres with "start year" and "primary title" colums

    Returns:
        budget_genre_df (pdDataFrame): joined dataframe with release year as datetime
    """
    temp_df = pd.DataFrame()
    temp_df = budgets_df.rename(columns={'movie': 'primary_title'})
    temp_df['release_date'] = temp_df['release_date'].map(
        lambda x: parser.parse(x))
    temp_df['start_year'] = temp_df['release_date'].dt.year
    budget_genre_df = pd.merge(temp_df, genres_df, on=[
                               'primary_title', 'start_year'], how='inner')
    budget_genre_df.drop(
        columns=['original_title', 'runtime_minutes'], inplace=True)
    return budget_genre_df


def money_to_int(df_column):
    """
    Turn a column with strings starting with '$' and potentially with ','s to int

    Arg:
        df_column (pdSeries): column with strings starting with '$' potentially containing commas

    Return:
        A column containing ints
    """
    return df_column.map(lambda x: int(x[1:].replace(',', '')))


def filter_by_year_budget(df, year, budget):
    """
    Removes data from the table prior to the input year and with bugdets lower than the input budget.
    Also adds a column representing the worldwide profit of each film in the df.

    Arg:
        df (pdDateFrame): a df containing columns labeled 'production_budget' and 'start_year'
        year (int): the year before which data will be dropped
        budget (int): the budget in dollars below which data will be dropped

    Return:
        df (pdDataFrame): df with values dropped and added profit column
    """
    df['production_budget'] = money_to_int(df['production_budget'])
    df = df[df['production_budget'] >= budget]
    df = df[df['start_year'] >= year]
    df['worldwide_gross'] = money_to_int(df['worldwide_gross'])
    df['domestic_gross'] = money_to_int(df['domestic_gross'])
    df['profit'] = df.worldwide_gross - df.production_budget
    return df


def make_profession_table(principles_df, names_df, profession):
    """
    Joins a table with names of workers on film with one containing their names. 
    Also drops 'birth_year', 'death_year', 'known_for_titles', 'job', 'characters'columns

    Arg:
        principles_df (pdDataFrame): a df containing 'nconst' column and 'category' column with professions
        names_df (pdDataFrame): a df containing 'nconst' column and names of people
        profession (str): a string naming a profession listed in the principles_df

    Return:
        name_profession_df (pdDataFrame): a df with names and movies of people of the specified profession with extra columns dropped
    """
    p_df = principles_df.drop(columns=['job', 'characters'])
    n_df = names_df.drop(
        columns=['birth_year', 'death_year', 'known_for_titles']).dropna()
    p_df.set_index('nconst', inplace=True)
    n_df.set_index('nconst', inplace=True)
    name_profession_df = p_df.join(n_df, how='left')
    name_profession_df = name_profession_df[name_profession_df["category"].str.contains(
        profession) == True]
    return name_profession_df


def make_complete_table(budget_genre_df, name_profession_df):
    """
    Joins tables containing budget and genre info with one containing names and profession info by the 'tconst' column
    Also drops 'ordering', 'primary_profession', 'id', 'start_year' columns

    Arg: 
        budget_genre_df (pdDataFrame): df with budget and genre info and a column 'tconst'
        name_profession_df (pdDataFrame): df with name and profession info and column 'tconst'

    Returns:
        complete_df (pdDataFrame): joined df with 'ordering', 'primary_profession', 'id', 'start_year' columns dropped
    """
    bg_df = budget_genre_df.set_index('tconst')
    np_df = name_profession_df.reset_index()
    np_df.set_index('tconst', inplace=True)
    complete_df = np_df.join(bg_df, how='left')
    complete_df = complete_df.drop(
        columns=['ordering', 'primary_profession', 'id', 'start_year'])
    complete_df.dropna(inplace=True)
    return complete_df


def list_genres(df):
    """
    Makes a list of the unique genres in a df.

    Arg:
        df (pdDataFrame): df with a 'genres' column where each row may contain comma seperated strings with multiple genre names

    Return:
        genre_list (list): a list of all the unique genres in the df
    """
    genre_list = []
    for entry in list(df['genres']):
        genres = entry.split(',')
        for genre in genres:
            if genre not in genre_list:
                genre_list.append(genre)
    return genre_list


def count_genres(genre_list, df):
    """
    Makes a dictionary counting all the movies of each genre in the genre_list.

    Arg:
        genre_list (list): a list of all the genres to be counted
        df (pdDataFrame): df with a 'genres' column where each row may contain comma seperated strings with multiple genre names

    Return:
        genre_count (dict): a dict with keys for each genre in the list 
            and values containing a count of how many movies are categorized as that genre
    """
    genre_count = dict.fromkeys(genre_list, 0)
    for entry in list(df['genres']):
        genres = entry.split(',')
        for genre in genres:
            genre_count[genre] += 1
    return genre_count


def genre_filter(df, genre):
    """
    Filters a dataframe to only include movies in the input genre

    Arg:
        df (pdDataFrame): a df with a 'genres' column where each row may contain comma seperated strings with multiple genre names
        genre (str): a str of the genre you wish to retain
    
    Return:
        df (pdDataFrame): a df containing only rows listed as in the genre
    """
    return df[df["genres"].str.contains(genre) == True]


def genre_stats(df, genres, n):
    """
    Makes a df with the mean and std of the profit in millions for each genre with more than n samples in the df.

    Arg:
        df (pdDataFrame): a df with 'genres' and 'profit' columns
        genres (list): a list of all the genres desired in the final df
        n (int): a count of examples a genre needs in the df to be included
    
    Return:
        genre_stats_df (pdDataFrame): a df containing the mean and std of the profits of each genre
    """
    m_s_dict = {}
    for genre in genres:
        profit_df = genre_filter(df, genre)["profit"]
        data_mean = profit_df.mean()/1000000
        data_std = profit_df.std()/1000000
        m_s_dict[genre] = [data_mean, data_std]
    genre_stats_df = pd.DataFrame.from_dict(m_s_dict)
    genre_stats_df.index = ['Mean Profit', 'Std of Profit']
    genre_stats_df = genre_stats_df.transpose().sort_values(
        'Mean Profit', ascending=False)
    genre_count = count_genres(genres, df)
    small_genre = [key for key in genre_count.keys() if genre_count[key] <= n]
    genre_stats_df.drop(small_genre, inplace=True)
    return genre_stats_df


def by_month_stats(df):
    """
    Filters a df to only contain columns with the month of the release date as an int
    and the mean and std of the profits for each month in millions of dollars

    Arg:
        df (pdDataFrame): a df with 'release_date' and 'profit' columns

    Return:
        release_df: a df with the mean and std of the profit in millions for each month represented as an int 
    """
    release_df = pd.DataFrame()
    release_df['release_month'] = df['release_date'].map(lambda x: x.month)
    release_df['profit'] = df['profit'].map(lambda x: x/1000000)
    mean_df = release_df.groupby(by='release_month').mean()
    release_df = release_df.groupby(by='release_month').std()
    release_df.rename(columns={'profit': 'Std of Profit'}, inplace=True)
    release_df['Mean Profit'] = mean_df['profit']
    return release_df


def profession_stats(df, genre):
    """
    Filters a df to only contain columns with and the mean and total of the profits in millions of dollars 
    for every film in the input genre grouped by the name of the person working on them.

    Arg:
        df (pdDataFrame): a df with 'genre', 'profit', and 'primary name' columns
        genre (str): the name of a genre to filter by
    
    Return:
        profession_stats_df (pdDataFrame): a df with mean and total profits earned by each person in that genre
    """
    profession_stats_df = pd.DataFrame()
    base_df = df[df['genres'].str.contains(genre) == True]
    base_df = base_df.drop(
        columns=['worldwide_gross', 'domestic_gross', 'production_budget'])
    profession_stats_df = base_df.groupby(by='primary_name').mean()
    profession_stats_df['profit'] = profession_stats_df['profit'].map(
        lambda x: x/1000000)
    profession_stats_df.rename(
        columns={'profit': 'Mean Profit'}, inplace=True)
    total_df = base_df.groupby(by='primary_name').sum()
    total_df['profit'] = total_df['profit'].map(lambda x: x/1000000)
    profession_stats_df['Total Profit'] = total_df['profit']
    profession_stats_df.sort_values(
        by='Mean Profit', ascending=False, inplace=True)
    return profession_stats_df
