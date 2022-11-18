import pandas as pd
import requests
import urllib.parse


def extract_wikipedia_pageview_statistics():
    movie_names = pd.read_csv('../handled_data/movie_names.csv')
    result = []
    
    for movie_name in movie_names['name'].unique():
        print(movie_name)

        query = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/" + \
            f"{urllib.parse.quote(movie_name.replace(' ', '_')).replace('/', '%2F')}/daily/2015070100/2022111500"

        response = requests.get(query, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        })
        pageview_stats = response.json()
        for day in pageview_stats['items']:
            result.append({'movie_name': movie_name, 'date': day['timestamp'], 'pageviews': day['views']})


    movie_wikipedia_pageviews = pd.DataFrame(result)
    movie_wikipedia_pageviews.to_csv('../handled_data/movies_wikipedia_pageviews.csv', index=False)


extract_wikipedia_pageview_statistics()