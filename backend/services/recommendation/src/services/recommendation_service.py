# from datetime import datetime, timedelta
import datetime
from services import combine_dict
from services import build_query_artists_with_limit, build_query_genres_with_limit, build_query_genres_by_year_with_limit
from services import get_similar_artists_query

def get_data_for_each_period(preferences):
    s = datetime.datetime.now().strftime("%d/%m/%Y")

    result = {
        "last_day": [],
        "last_week": [],
        "other": []
    }

    for elem in preferences['preferences']:
        elem_date = datetime.datetime.strptime(elem, "%d/%m/%Y")
        diff = datetime.datetime.strptime(s, "%d/%m/%Y") - elem_date
        if diff.days <= 1:
            result["last_day"].append(preferences['preferences'][elem])
        elif diff.days <= 7:
            result["last_week"].append(preferences['preferences'][elem])
        else:
            result["other"].append(preferences['preferences'][elem])
    return result

def get_recommendation_for_user(preferences):
    data = get_data_for_each_period(preferences)

    result = {
        "last_day": {
            "artists": {},
            "genres": {},
            "years": {}
        },
        "last_week": {
            "artists": {},
            "genres": {},
            "years": {}
        },
        "other": {
            "artists": {},
            "genres": {},
            "years": {}
        }
    }
    for period in data.keys():
        if len(data[period]) > 0:
            for elem in data[period]:
                for key_field in elem.keys():
                    for concrete_elem in elem[key_field].keys():
                        if concrete_elem in result[period][key_field]:
                            result[period][key_field][concrete_elem] += elem[key_field][concrete_elem]
                        else:
                            result[period][key_field][concrete_elem] = elem[key_field][concrete_elem]
    return result


def get_recommendation_per_periods(preferences):
    no_recommendation = 100
    no_recommendation_last_day = 30
    no_recommendation_last_week = 50
    no_recommendation_other = 20
    queries_to_run = []
    try:
        if 'last_day' in preferences:
            last_day_preferences = preferences['last_day']
            if 'artists' in last_day_preferences:
                total_no_artists = sum(last_day_preferences['artists'].values())
                for artist in last_day_preferences['artists']:
                    limit = int((last_day_preferences['artists'][artist] / total_no_artists) * no_recommendation_last_day)
                    queries_to_run.append(build_query_artists_with_limit(artist, limit))
            if 'genres' in last_day_preferences:
                total_no_genres = sum(last_day_preferences['genres'].values())
                for genre in last_day_preferences['genres']:
                    limit = int((last_day_preferences['genres'][genre] / total_no_genres) * no_recommendation_last_day)
                    queries_to_run.append(build_query_genres_with_limit(genre, limit))
            if 'years' in last_day_preferences:
                total_no_years = sum(last_day_preferences['years'].values())
                for year in last_day_preferences['years']:
                    limit = int((last_day_preferences['years'][year] / total_no_years) * no_recommendation_last_day)
                    queries_to_run.append(build_query_genres_by_year_with_limit(year, limit))
        elif 'last_week' in preferences:
            last_week_preferences =preferences['last_week']
            if 'artists' in last_week_preferences:
                total_no_artists = sum(last_week_preferences['artists'].values())
                for artist in last_week_preferences['artists']:
                    limit = int((last_week_preferences['artists'][artist] / total_no_artists) * no_recommendation_last_week)
                    queries_to_run.append(build_query_artists_with_limit(artist, limit))
            if 'genres' in last_week_preferences:
                total_no_genres = sum(last_week_preferences['genres'].values())
                for genre in last_week_preferences['genres']:
                    limit = int((last_week_preferences['genres'][genre] / total_no_genres) * no_recommendation_last_week)
                    queries_to_run.append(build_query_genres_with_limit(genre, limit))
            if 'years' in last_week_preferences:
                total_no_years = sum(last_week_preferences['years'].values())
                for year in last_week_preferences['years']:
                    limit = int((last_week_preferences['years'][year] / total_no_years) * no_recommendation_last_week)
                    queries_to_run.append(build_query_genres_by_year_with_limit(year, limit))
        elif 'other' in preferences:
            other_preferences = preferences['other']
            if 'artists' in other_preferences:
                total_no_artists = sum(other_preferences['artists'].values())
                for artist in other_preferences['artists']:
                    limit = int((other_preferences['artists'][artist] / total_no_artists) * no_recommendation_other)
                    queries_to_run.append(build_query_artists_with_limit(artist, limit))
            if 'genres' in other_preferences:
                total_no_genres = sum(other_preferences['genres'].values())
                for genre in other_preferences['genres']:
                    limit = int((other_preferences['genres'][genre] / total_no_genres) * no_recommendation_other)
                    queries_to_run.append(build_query_genres_with_limit(genre, limit))
            if 'years' in other_preferences:
                total_no_years = sum(other_preferences['years'].values())
                for year in other_preferences['years']:
                    limit = int((other_preferences['years'][year] / total_no_years) * no_recommendation_other)
                    queries_to_run.append(build_query_genres_by_year_with_limit(year, limit))
    except Exception as e:
        print(e)

    return queries_to_run


def get_recommendation_for_user_by_artists(preferences):
    queries_to_run = []
    for timestamp in preferences:
        total_no_artists = sum(preferences[timestamp]['artists'].values())
        for artist in preferences[timestamp]['artists']:
            limit = int((preferences[timestamp]['artists'][artist] / total_no_artists) * 100)
            queries_to_run.append(build_query_artists_with_limit(artist, limit))
            queries_to_run.extend(get_similar_artists_query([artist])[:3])
    return queries_to_run

def get_recommendation_for_user_by_genres(preferences):
    queries_to_run = []
    for timestamp in preferences:
        total_no_genres = sum(preferences[timestamp]['genres'].values())
        for genre in preferences[timestamp]['genres']:
            limit = int((preferences[timestamp]['genres'][genre] / total_no_genres) * 100)
            queries_to_run.append(build_query_genres_with_limit(genre, limit))
    return queries_to_run