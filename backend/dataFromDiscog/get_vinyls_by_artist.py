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
ids = []

with open('artists.txt', 'r', encoding='utf-8') as filehandle:
    for line in filehandle:
        currentPlace = line[:-1]
        artists_list.append(currentPlace)

vinyls_uniques = set()
for artist in artists_list:
    count = 0
    print(artist)
    vinyls = d.search(format='Vinyl', artist=artist, per_page=100, page=1)
    print(vinyls.pages)
    if count <= 4:
        for page_number in range(1, min(5, vinyls.pages + 1)):
            vinyls_temp = vinyls.page(page_number)
            for vinyl in vinyls_temp:
                try:
                    if vinyl.title != '' and len(vinyl.tracklist) > 0 and  len(vinyl.genres) > 0 and vinyl.year != 0:
                        ok = 0
                        for track in vinyl.tracklist:
                            if len(track.artists) > 0:
                                ok = 1
                                break
                        if ok == 1:
                            if vinyl.title not in vinyls_uniques:
                                vinyls_uniques.add(vinyl.title)
                                count += 1
                                release_uri = mo["#vinyl-" + str(vinyl.id)]
                                vinyl_graph = Graph()
                                vinyl_graph.add((release_uri, RDF.type, mo.Vinyl))
                                vinyl_graph.add((release_uri, dc['title'], Literal(vinyl.title)))
                                vinyl_graph.add((release_uri, mo['genre'], Literal(vinyl.genres)))
                                if vinyl.year != 0:
                                    vinyl_graph.add((release_uri, dc['date'], Literal(vinyl.year)))
                                if vinyl.images:
                                    vinyl_graph.add((release_uri, mo['imageUrl'], Literal(vinyl.images[0]['uri'])))
                                count_song = 0
                                for track in vinyl.tracklist:
                                    if count_song <= 7:
                                        if track.artists is not None and len(track.artists) > 0:
                                            count_song += 1
                                            song_graph = Graph()
                                            song_uri = mo[
                                                "#song-" +
                                                track.title.replace(' ', '_').lower().replace('"', '').replace('.','').replace('\'', '').replace('<', '').replace('>', '')
                                            + track.artists[0].name.replace(' ', '_').lower().replace('"', '').replace('.','').replace('\'', '').replace('<', '').replace('>', '')]

                                            song_graph.add((song_uri, RDF.type, mo.Song))
                                            song_graph.add((song_uri, dc['title'], Literal(song_uri)))
                                            if track.duration != 0 and track.duration is not None and track.duration != '':
                                                song_graph.add((song_uri, mo['duration'], Literal(track.duration)))

                                            if track.artists is not None and len(track.artists) > 0:
                                                for track_artist in track.artists:
                                                    if track_artist.name != '':
                                                        song_graph.add((song_uri, mo['artist'], Literal(track_artist.name)))
                                                        vinyl_graph.add((release_uri, foaf['name'], Literal(track_artist.name)))
                                            vinyl_graph.add((release_uri, mo['track'], song_uri))
                                ttl_data = vinyl_graph.serialize(format='turtle')
                                with open('vinyls_super.ttl', 'a', encoding='utf-8') as ttl_file:
                                    ttl_file.write(ttl_data)
                except Exception as e:
                    print(e)
                    continue