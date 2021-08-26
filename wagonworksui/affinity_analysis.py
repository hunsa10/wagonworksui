import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from sklearn.cluster import KMeans
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from gensim.models import Word2Vec
from get_data import get_month_data
from utils import convert_date, convert_time, xl_to_py_date, xl_to_py_time, format_date, format_time,


def get_csv(csv):
    df = pd.read_csv(csv, low_memory = False)

    # format date columns
    df.loc[:,'Plan_GI_Date'] = format_date(df, date_col ='Plan_GI_Date')
    df.loc[:,'Act_GI_Date'] = format_date(df, date_col ='Act_GI_Date')
    df.loc[:,'Del_Creat_Date'] = format_date(df, date_col ='Del_Creat_Date')

    # format date columns
    df.loc[:,'Del_Creat_Time'] = format_time(df, time_col = 'Del_Creat_Time')

    return df


def filter_sku():
    # count no. of orders that only have one item
    df = get_csv(csv)[['Del_NumA', 'SKU_A']]
    df_articles_counted = df.groupby('Del_NumA').count()
    order_list = df_articles_counted[df_articles_counted['SKU_A'] >1].index.tolist()

    # removed orders that only contains single item and items that are only ever purchased once
    df_multiple_articles = df[df['Del_NumA'].isin(order_list)]
    df_multiple_buys = df_multiple_articles[df_multiple_articles['SKU_A'].map(df_multiple_articles['SKU_A'].value_counts()>1)]
    df_multiple_buys['SKU_A_space'] = df_multiple_buys['SKU_A'] + ' '
    return df_multiple_buys


def concat_sku():
    # combine article codes of the same order into one cell
    df_multiple_buys = filter_sku()
    df_article_string = df_multiple_buys.groupby('Del_NumA').sum()
    return df_article_string


def w2v_df():
    '''fit data to word2vec model'''

    df_multiple_buys = filter_sku()
    df_article_string = concat_sku()
    X = [text_to_word_sequence(article) for article in df_article_string['SKU_A_space']]
    word2vec = Word2Vec(sentences=X)
    df_article_embed = df_multiple_buys[df_multiple_buys['SKU_A'].str.lower().isin(list(word2vec.wv.vocab.keys()))]

    # create column for embedded articles
    df_article_embed['article_embed'] = df_article_embed['SKU_A'].apply(lambda x: word2vec.wv[x.lower()])
    return df_article_embed


# split aritcle embed into multiple columns and assign to variable X
def split_cols():
    df_article_embed = w2v_df()
    df_splited_cols = df_article_embed['article_embed'].apply(pd.Series)
    X = df_splited_cols.to_numpy()
    return X

# km model to use to get clusters of products
def km_model():
    ''' fit kmeans model and calculate distance of each node to the centroid'''
    X = split_cols()
    clustering = KMeans(n_clusters=20, n_init=10, random_state=1)
    clustering.fit(X)
    X_dist = clustering.transform(X) # calculate distance of each node to the centroid

    # create new columns for sum of distance and clustering labels
    df_article_embed = w2v_df()
    df_article_embed['X_dist'] = X_dist.sum(axis=1).round(2)
    df_article_embed['labels'] = clustering.labels_
    df_article_unique = df_article_embed.drop_duplicates('SKU_A')
    return df_article_unique


# km model to use to get 10 products frequently bought together
def kmeans_model():
    X = split_cols()
    clustering = KMeans(n_clusters=20, n_init=10,
                        random_state=1)
    clustering.fit(X)
    return clustering

def label_df():
    clustering = kmeans_model()
    df_article_embed = w2v_df()
    df_article_embed['labels'] = clustering.labels_
    labeled_df = df_article_embed.drop_duplicates('SKU_A')
    return labeled_df


def get_label(sku): # return label of the input sku and its vector
    clustering = kmeans_model()
    labeled_df = label_df()
    test = labeled_df.loc[labeled_df['SKU_A'] == sku, ['article_embed', 'labels']]
    test_label = int(test[['labels']].values)
    test_centroid = clustering.cluster_centers_[test_label]
    test_v = test['article_embed'].values[0]
    return test_label, test_centroid, test_v


def get_cluster_sku(sku): # return df of all items in the same label as the entered sku
    labeled_df = label_df()
    test_label = get_label(sku)[0]
    test_df = labeled_df.loc[labeled_df['labels'] == test_label, ['SKU_A', 'article_embed']]
    test_df.reset_index(inplace=True, drop=True)
    return test_df


# return clusters of products
def clustered_articles(max_articles=10, max_clusters=10):
    '''final result of article clusters that are most commonly purchased together'''

    # find clusters that only have 2-5 SKUs
    df_article_unique = km_model()
    cluster_counted = df_article_unique.value_counts('labels')
    small_clusters = cluster_counted[(cluster_counted<=max_clusters) & (cluster_counted>1)]

    # create dataframe for small clusters (2-5 SKUs each cluster)
    df_small_clusters = df_article_unique[df_article_unique['labels'].isin(small_clusters.index)]

    # group by labels and find 5 clusters with lowest average distance
    avg_dist_lowest = df_small_clusters.groupby('labels').mean().sort_values('X_dist').iloc[:max_clusters]
    df_clustered_articles = df_small_clusters[df_small_clusters['labels'].isin(avg_dist_lowest.index)]

    # group sku per cluster as items commonly purhcased together
    df_clustered_articles['SKU_A_space'] = df_clustered_articles['SKU_A'] + ' '
    df_results = pd.DataFrame(df_clustered_articles.groupby('labels')['SKU_A_space'].sum())
    return df_results


# return a list of the closet data points to the entered sku
def purchased_together(sku):
    test_df =get_cluster_sku(sku)
    test_v = get_label(sku)[1]
    dist_sorted = test_df['article_embed'].apply(lambda x: euclidean(test_v, x)).sort_values()

    # index of 10 shortest distance
    dist_sort = list(dist_sorted[1:11].index)
    item_list = test_df.iloc[dist_sort]['SKU_A']
    return pd.DataFrame(item_list).reset_index(drop=True).rename(columns={'SKU_A': 'SKU'})
