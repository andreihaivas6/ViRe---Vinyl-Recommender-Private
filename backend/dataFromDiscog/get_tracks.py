from rdflib import Graph, Namespace, Literal, RDF

import discogs_client
mo = Namespace("http://purl.org/ontology/mo/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
d = discogs_client.Client('ExampleApplication/0.1',
                                  user_token='QeRscQhmoTVgfEqFitPAMOfDUSmmPNAevdppFRKD',
                                  )

artists_list = []
genres_list = []
songs_list = []

song_ids = set()
releases = d.search(type='release', per_page=100)
print("My pages: ", releases.pages)
for page_number in range(1, releases.pages + 1):
    print(page_number)
    releases_temp = releases.page(page_number)
    print(len(releases_temp))
    for release in releases_temp:
        ok = False
        if release.title is not None and release.artists is not None and len(release.artists) > 0 and release.genres is not None and len(release.genres) > 0 and release.tracklist is not None and len(release.tracklist) > 0 and release.year is not None:
            ok = True
        if ok:
            for track in release.tracklist:
                song_graph = Graph()
                song_id = track.title.replace(' ', '_').lower().replace('"', '').replace('.','').replace('\'', '').replace('<', '').replace('>', '') + '-' + release.artists[0].name.replace(' ', '_').lower().replace('"', '').replace('.','').replace('\'', '').replace('<', '').replace('>', '')
                if song_id not in song_ids:
                    song_ids.add(song_id)
                    song_uri = mo[ "#song-" + song_id]
                    song_graph.add((song_uri, RDF.type, mo.Song))

                    song_graph.add((song_uri, dc['title'], Literal(track.title)))
                    # year 
                    song_graph.add((song_uri, dc['date'], Literal(release.year)))
                    # genre
                    song_graph.add((song_uri, mo['genre'], Literal(release.genres)))
                    # title album 
                    song_graph.add((song_uri, mo['album'], Literal(release.title)))
                    # artists
                    for artist in release.artists:
                        song_graph.add((song_uri, mo['artist'], Literal(artist.name)))

                    ttl_data = song_graph.serialize(format='turtle')
                    with open('total_songs.ttl', 'a', encoding='utf-8') as ttl_file:
                        ttl_file.write(ttl_data)


with open('my_artists.txt', 'r', encoding='utf-8') as filehandle:
    for line in filehandle:
        currentPlace = line[:-1]
        artists_list.append(currentPlace)

for artist in artists_list:
    releases = d.search(type='release', artist=artist, per_page=100)
    print(releases.pages)
    for page_number in range(1, releases.pages + 1):
        print(page_number)
        releases = releases.page(page_number)
        print(len(releases))
        for release in releases:
            ok = False
            if release.title is not None and release.artists is not None and len(release.artists) > 0 and release.genres is not None and len(release.genres) > 0 and release.tracklist is not None and len(release.tracklist) > 0 and release.year is not None:
                ok = True
            if ok:
                for track in release.tracklist:
                    song_graph = Graph()
                    song_id = track.title.replace(' ', '_').lower().replace('"', '').replace('.','').replace('\'', '').replace('<', '').replace('>', '') + '-' + release.artists[0].name.replace(' ', '_').lower().replace('"', '').replace('.','').replace('\'', '').replace('<', '').replace('>', '')
                    if song_id not in song_ids:
                        song_ids.add(song_id)
                        song_uri = mo[ "#song-" + song_id]
                        song_graph.add((song_uri, RDF.type, mo.Song))

                        song_graph.add((song_uri, dc['title'], Literal(track.title)))
                        # year 
                        song_graph.add((song_uri, dc['date'], Literal(release.year)))
                        # genre
                        song_graph.add((song_uri, mo['genre'], Literal(release.genres)))
                        # title album 
                        song_graph.add((song_uri, mo['album'], Literal(release.title)))
                        # artists
                        for artist in release.artists:
                            song_graph.add((song_uri, mo['artist'], Literal(artist.name)))

                        ttl_data = song_graph.serialize(format='turtle')
                        with open('total_songs.ttl', 'a', encoding='utf-8') as ttl_file:
                            ttl_file.write(ttl_data)
