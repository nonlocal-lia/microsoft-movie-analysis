import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dateutil import parser
from datetime import date

def make_budget_genre_table(budgets_df, genres_df):
    """
    Takes in two pandas dataframes containing budgets, release date
    and genre info and joins them by movie title and release year
    """
    budgets_df.rename(columns = {'movie' : 'primary_title'}, inplace=True)
    budgets_df['release_date'] = budgets_df['release_date'].map(lambda x: parser.parse(x))
    budgets_df['start_year'] = budgets_df['release_date'].dt.year
    budget_genre_df = pd.merge(budgets_df, genres_df, on = ['primary_title', 'start_year'], how='inner')
    budget_genre_df.drop(columns = ['original_title', 'runtime_minutes'], inplace=True)
    return budget_genre_df

def money_to_int(df_column):
    """
    Takes in a pandas df column with strings representing dollar and returns the column in int
    """
    return df_column.map(lambda x: int(x[1:].replace(',','')))

def filter_by_year_budget(df, year, budget):
    """
    Takes in a pd.df, a year in int, and a budget in int, and returns
    a df removing all the rows prior to that year and with less than that budget.
    """
    df['production_budget'] = money_to_int(df['production_budget'])
    df = df[df['production_budget'] >= budget]
    df = df[df['start_year'] >= year]
    df['worldwide_gross'] = money_to_int(df['worldwide_gross'])
    df['domestic_gross'] = money_to_int(df['domestic_gross'])
    df['profit'] = df.worldwide_gross - df.production_budget
    return df

def make_director_table(principles_df, names_df, profession):
    """
    Takes in two pandas dataframes containing talent names and the movies they worked on,
    and joins them, drops irrelevant columns and filters by the input profession string
    """
    principles_df = principles_df.drop(columns = ['job','characters'])
    names_df = names_df.drop(columns = ['birth_year', 'death_year', 'known_for_titles']).dropna()
    principles_df.set_index('nconst', inplace=True)
    names_df.set_index('nconst', inplace=True)
    name_profession_df = principles_df.join(names_df, how='left')
    name_profession_df = name_profession_df[name_profession_df["category"].str.contains(profession)==True]
    return name_profession_df

def make_complete_table(budget_genre_df, name_profession_df):
    """
    Takes in two pandas dataframes containing budgets/genre info and profession/name data
    and joins them by the title key of the movies, and drops irrelevant columns
    """
    budget_genre_df.set_index('tconst', inplace=True)
    name_profession_df.reset_index(inplace = True)
    name_profession_df.set_index('tconst', inplace=True)
    complete_df = name_profession_df.join(budget_genre_df, how='left')
    complete_df = complete_df.drop(columns = ['ordering','primary_profession', 'id', 'start_year'])
    complete_df.dropna(inplace = True)
    return complete_df

def list_genres(df):
    """
    Takes a pandas dataframe and returns a list of the unique genres in the df.
    """
    genre_list = []
    for entry in list(df['genres']):
        genres = entry.split(',')
        for genre in genres:
            if genre not in genre_list:
                genre_list.append(genre)
    return genre_list

def count_genres(genre_list, df):
    genre_count = dict.fromkeys(genre_list, 0)
    for entry in list(df['genres']):
        genres = entry.split(',')
        for genre in genres:
            genre_count[genre] += 1
    return genre_count

def genre_filter(df, genre):
    """
    Takes a pd dataframe and filters the dataframe to only contain those movies of the specified genre
    """
    return df[df["genres"].str.contains(genre)==True]

def genre_stats(df, genres, n):
    """
    Takes a dataframe, a list of all the desired genres, and a miminum sample number
    and returns a df with the mean and std of the profit in millions
    for each genre with more than n samples in the df.
    """
    m_s_dict = {}
    for genre in genres:
        profit_df = genre_filter(df, genre)["profit"]
        data_mean = profit_df.mean()/1000000
        data_std = profit_df.std()/1000000
        m_s_dict[genre] = [data_mean, data_std]
    genre_stats_df = pd.DataFrame.from_dict(m_s_dict)
    genre_stats_df.index = ['Mean Profit', 'Std of Profit']
    genre_stats_df = genre_stats_df.transpose().sort_values('Mean Profit', ascending = False)
    genre_count = count_genres(genres, df)
    small_genre = [key for key in genre_count.keys() if genre_count[key] <= n]
    genre_stats_df.drop(small_genre, inplace=True)
    return genre_stats_df

def by_month_stats(df):
    """
    Takes in a pandas dataframe, groups it by month or release,
    calculates the mean and std of profit by month of release,
    and returns a df filtered to only contain columns with the month of the release date
    and the mean and std of the profits for each monthin millions of dollars
    """
    release_df = pd.DataFrame()
    release_df['release_month'] = df['release_date'].map(lambda x: x.month)
    release_df['profit'] = df['profit'].map(lambda x: x/1000000)
    release_df.reset_index(inplace = True)
    release_df.drop(columns = ['tconst'])
    mean_df = release_df.groupby(by = 'release_month').mean()
    release_df = release_df.groupby(by = 'release_month').std()
    release_df.rename(columns = {'profit' : 'Std of Profit'}, inplace=True)
    release_df['Mean Profit'] = mean_df['profit']
    return release_df

def profession_stats(df, genre):
    """
    Takes in a pandas dataframe, filters it by genre, groups it by the names of the people,
    and calculates the mean and total profit made by each person
    and returns a df filtered to only contain columns with 
    and the mean and std of the profits for each named person
    """
    profession_stats_df = pd.DataFrame()
    base_df = df[df['genres'].str.contains(genre)==True]
    base_df = base_df.drop(columns = ['worldwide_gross', 'domestic_gross', 'production_budget'])
    profession_stats_df = base_df.groupby(by='primary_name').mean()
    profession_stats_df['profit'] = profession_stats_df['profit'].map(lambda x: x/1000000)
    profession_stats_df.rename(columns = {'profit': 'Mean Profit in Millions'}, inplace = True)
    total_df = base_df.groupby(by='primary_name').sum()
    total_df['profit'] = total_df['profit'].map(lambda x: x/1000000)
    profession_stats_df['Total Profit in Millions'] = total_df['profit']
    profession_stats_df.sort_values(by='Mean Profit in Millions', ascending = False, inplace = True)
    return profession_stats_df

