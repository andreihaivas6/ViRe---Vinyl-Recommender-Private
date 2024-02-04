
from services import get_similar_artists_by_name


def build_query_artists(artist_name):
    query = """
SELECT DISTINCT ?vinyl ?title ?artist ?genre
    WHERE {
        ?vinyl a ns1:Vinyl ;
        dc:title ?title ;
        ns1:genre ?genre ;
        ns1:imageUrl ?imageUrl ;
        dc:date ?date ;
        ns1:track ?track ;
        foaf:name ?artist .
        """
    query += f"FILTER (UCASE(?artist) = UCASE('{artist_name}'))\n"
    query += "} LIMIT 10"

    return query

def get_similar_artists_query(artist_name):
    queries = []
    for artist in artist_name:
        similar_artists = get_similar_artists_by_name(artist)
        
        for similar_artist in similar_artists:
            queries += build_query_artists(similar_artist)
    return queries

def sparql_query_builder_for_preferences(preferences):
    # preferences = {'like': {}, 'dislike': {'before': 2020,'genre':{'hip-hop'}}, 'love': {'artist': {'verdi', 'rossini','the beatles'}, 'before': 2020, 'after': 2014}, 'hate': {}, 'sentiments': []}
    query_base = """
SELECT DISTINCT ?vinyl ?title ?artist ?genre
    WHERE {
        ?vinyl a ns1:Vinyl ;
        dc:title ?title ;
        ns1:genre ?genre ;
        ns1:imageUrl ?imageUrl ;
        dc:date ?date ;
        ns1:track ?track ;
        foaf:name ?artist .
        """

    ok = False
    
    date_query = ""
    exclude_query = ""
    date_query_exclude = ""
    ok_date = False
    ok_exclude = False
    ok_date_exclude = False
    exclude_query = ""
    loves_artist = False
    artists_name = []

    for sentiment in preferences:
        ok_filter = False
        if sentiment in ['like', 'love']:
            if not ok:
                query_base += "\nFILTER (\n"
                ok = True

            for entity in preferences[sentiment]:
                # artist, genre, before, after
                if entity in ['artist', 'genre']:
      
                    if entity == 'artist':
                        loves_artist = True
                        artists_name += list(preferences[sentiment][entity])
                        if ok_filter:
                            query_base += "&& "
                            query_base += "UCASE(?artist) IN ('" + "',UCASE( '".join(preferences[sentiment][entity]) + "'))'\n"
                        else:
                            query_base += "UCASE(?artist) IN (UCASE('" + "'),UCASE('".join(preferences[sentiment][entity]) + "'))\n"
                            ok_filter = True
                
                    elif entity == 'genre':
                        if ok_filter:
                            query_base += "&& ("
                            for genre in preferences[sentiment][entity]:
                                query_base += f"REGEX(?genre,\"{genre}\",\"i\") || " 
                            query_base = query_base[:-3] + ")\n"
                        else:
                            query_base += "("

                            for genre in preferences[sentiment][entity]:
                                query_base += f"REGEX(?genre,\"{genre}\",\"i\") || " 
                            query_base = query_base[:-3] + ")\n"
                            ok_filter = True
                  
                elif entity in ['before', 'after']:
                    if not ok_date:
                        if entity == 'before':
                            date_query += f"(?date < {preferences[sentiment][entity]})\n"
                        elif entity == 'after':
                            date_query += f"(?date > {preferences[sentiment][entity]})\n"
                        ok_date = True
                    else:
                        if entity == 'before':
                            date_query += f"&& (?date < {preferences[sentiment][entity]})\n"
                        elif entity == 'after':
                            date_query += f"&& (?date > {preferences[sentiment][entity]})\n"
        else:
             for entity in preferences[sentiment]:
                if entity in ['artist', 'genre']:
                    if entity == 'artist':
                        if ok_exclude:
                            exclude_query += "&& "
                            exclude_query += "UCASE(?artist) NOT IN ('" + "',UCASE( '".join(preferences[sentiment][entity]) + "'))'\n"
                        else:
                            exclude_query += "UCASE(?artist) NOT IN (UCASE('" + "'),UCASE('".join(preferences[sentiment][entity]) + "'))\n"
                            ok_exclude = True
                
                    elif entity == 'genre':
                        if ok_exclude:
                            exclude_query += "&& ("
                            for genre in preferences[sentiment][entity]:
                                exclude_query += f"(!REGEX(?genre,\"{genre}\",\"i\")) || " 
                            exclude_query = exclude_query[:-3] + ")\n"
                        else:
                            exclude_query += "("
                            for genre in preferences[sentiment][entity]:
                                exclude_query += f"(!REGEX(?genre,\"{genre}\",\"i\")) || " 

                            exclude_query = exclude_query[:-3] + ")\n"

                            ok_exclude = True
                elif entity in ['before', 'after']:
                    if not ok_date_exclude:
                        if entity == 'before':
                            date_query_exclude += f"(?date > {preferences[sentiment][entity]})\n"
                        elif entity == 'after':
                            date_query_exclude += f"(?date < {preferences[sentiment][entity]})\n"
                        ok_date_exclude = True
                    else:
                        if entity == 'before':
                            date_query_exclude += f"&& (?date > {preferences[sentiment][entity]})\n"
                        elif entity == 'after':
                            date_query_exclude += f"&& (?date < {preferences[sentiment][entity]})\n"

    if date_query_exclude!="":
        exclude_query ="(" + exclude_query + " || " + date_query_exclude + ")\n" 

    if date_query!="":
        query_base += "&& " + date_query + "\n"
        if exclude_query!="":
            query_base += "&& " + exclude_query + ")}\n"
        else:
            query_base += ")}\n"
    else:
        if exclude_query!="":
            query_base += "&& " + exclude_query + ")}\n"
        else:
            query_base += "}\n"
    if loves_artist:
        get_similar_artists_query(artists_name)

    return query_base
                # build query
                # call sparql service
                # get recommendations
                