import pandas as pd
import requests
import urllib.parse

from multiprocessing import Pool
import tqdm


def get_pageview_statistics(movie_name):
    result = []
    try:
        query = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/" + \
            f"{urllib.parse.quote(movie_name.replace(' ', '_')).replace('/', '%2F')}/monthly/2015070100/2022120300"

        response = requests.get(query, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        })
        pageview_stats = response.json()
        for month in pageview_stats['items']:
            result.append({'movie_name': movie_name, 'date': month['timestamp'], 'pageviews': month['views']})
    except:
        print(f'problem: {movie_name}')

    return result


def extract_wikipedia_pageview_statistics():
    movie_names = pd.read_csv('./handled_data/movie_names.csv')

    pool = Pool(processes=12)

    results = []
    for result in tqdm.tqdm(pool.imap_unordered(get_pageview_statistics, movie_names['name'].unique()), total=len(movie_names['name'].unique())):
        results.append(result)

    results = sum(results, [])

    movie_wikipedia_pageviews = pd.DataFrame(results)
    movie_wikipedia_pageviews.to_csv('./handled_data/movies_wikipedia_pageviews_raw.csv', index=False)


def aggregate_wikipedia_pageview_statistics():
    movie_names = pd.read_csv('./handled_data/movie_names.csv')
    movie_wikipedia_pageviews = pd.read_csv('./handled_data/movies_wikipedia_pageviews_raw.csv')

    year_min = movie_names['release_year'].min()
    year_max = 2022

    movie_wikipedia_pageviews = movie_wikipedia_pageviews[movie_wikipedia_pageviews['date'] >= 2021120100]
    movie_wikipedia_pageviews = movie_wikipedia_pageviews \
        .groupby(['movie_name']) \
        .apply(lambda pv: pv['pageviews'].mean() * (1 + ((year_max - movie_names[movie_names['name'] == pv['movie_name'].iloc[0]]['release_year'].iloc[0]) / (year_max - year_min)))) \
        .reset_index()

    movie_wikipedia_pageviews.to_csv('./handled_data/movies_wikipedia_pageviews.csv', index=False)


if __name__ == '__main__':
    # extract_wikipedia_pageview_statistics()
    aggregate_wikipedia_pageview_statistics()
