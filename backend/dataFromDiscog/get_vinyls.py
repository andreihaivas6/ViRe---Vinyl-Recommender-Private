from rdflib import Graph, Namespace, Literal, RDF

import discogs_client
mo = Namespace("http://purl.org/ontology/mo/")
dc = Namespace("http://purl.org/dc/elements/1.1/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")

d = discogs_client.Client('ExampleApplication/0.1',
                                  user_token='QeRscQhmoTVgfEqFitPAMOfDUSmmPNAevdppFRKD',
                                  )
artists_list = set()
genres_list = set()
songs_list = set()
vinyl_list = set()

ids = []
vinyls = d.search(format='Vinyl', page=2, per_page=1000)
vinyl_graph = Graph()
artist_graph = Graph()
song_graph = Graph()

def add_genres(vinyl, release_uri, ok):
    global genres_list
    global vinyl_graph
    if vinyl.genres is not None:
        for genre in vinyl.genres:
            if genre.lower() not in genres_list:
                genre = genre.lower()
                genres_list.add(genre)
                with open('genres.txt', 'a', encoding='utf-8') as filehandle:
                    filehandle.write(f'{genre}\n')
            if ok:
                vinyl_graph.add((release_uri, mo['genre'], Literal(genre.lower())))

def add_artists(vinyl, release_uri, ok):
    global artist_graph
    global artists_list
    global vinyl_graph
    current_artists = []
    try:
        for artist in vinyl.artists:
            if artist.name not in artists_list and artist.name != '':
                artists_list.add(artist.name)
                current_artists.append(artist.name)
                with open('artists.txt', 'a', encoding='utf-8') as filehandle:
                    filehandle.write(f'{artist.name}\n')
                release_uri_artist = mo["#artist-" + str(artist.id)]
                artist_graph.add((release_uri_artist, RDF.type, mo.Artist))
                artist_graph.add((release_uri_artist, foaf['name'], Literal(artist.name)))

                try:
                    if artist.images is not None and len(artist.images) > 0:
                        if artist.images[0]['uri'] is not None:
                            artist_graph.add((release_uri_artist, mo['imageUrl'], Literal(artist.images[0]['uri'])))
                except:
                    print("error adding artist to graph")
                ttl_data = artist_graph.serialize(format='turtle')  # , destination='music.ttl')
                with open('artists-3.ttl', 'a', encoding='utf-8') as ttl_file:
                    ttl_file.write(ttl_data)
            if ok:
                vinyl_graph.add((release_uri, foaf['name'], Literal(artist.name)))
        return current_artists
    except Exception as e:
        print(e)
        print("error adding artist to vinyl")
        return []
def add_songs(vinyl, release_uri, ok, current_artists):
    global song_graph
    global songs_list
    # print("hey",songs_list)
    for song in vinyl.tracklist:
        current_title = song.title.replace(' ', '_').lower().replace('"', '').replace('.', '').replace('\'','').replace('<','').replace( '>', '')

        if song.title != '' and (current_title, song.duration) not in songs_list:
            songs_list.add( (current_title, song.duration) )
            try:
                song_uri = mo["#song-" + current_title]
                song_graph.add((song_uri, RDF.type, mo.Song))
                song_graph.add((song_uri, dc['title'], Literal(song.title)))
                if song.duration != 0 and song.duration is not None and song.duration != '':
                    song_graph.add((song_uri, mo['duration'], Literal(song.duration)))
                if vinyl.genres is not None and len(vinyl.genres) > 0:
                    song_graph.add((song_uri, mo['genre'], Literal(vinyl.genres[0])))
                if vinyl.year != 0:
                    song_graph.add((song_uri, dc['date'], Literal(vinyl.year)))
                if current_artists is not None and len(current_artists) > 0:
                    for artist in current_artists:
                        song_graph.add((song_uri, mo['artist'], Literal(artist)))
                ttl_data = song_graph.serialize(format='turtle')
                with open('song-3.ttl', 'a', encoding='utf-8') as ttl_file:
                    ttl_file.write(ttl_data)
                if ok:
                    vinyl_graph.add((release_uri, mo['track'], song_uri))
            except Exception as e:
                print(e)
                print(1)
                print("error adding song to vinyl")

def get_all_vinyl_releases():
    global vinyl_graph
    global artist_graph
    global song_graph

    try:
        for page_number in range(1, vinyls.pages + 1):
            print("page: ", page_number)
            vinyls_temp = vinyls.page(page_number)
            print("No vinyls:",len(vinyls_temp))
            try:
                for i in range(0, len(vinyls_temp)):
                    vinyl = vinyls_temp[i]
                    release_uri = mo["#vinyl-" + str(vinyl.id)]
                    vinyl_graph = Graph()
                    artist_graph = Graph()
                    song_graph = Graph()
                    try:
                        ok = False

                        try:
                            if vinyl.title != '' and vinyl.genres is not None and vinyl.tracklist is not None and vinyl.artists is not None:
                                if (vinyl.title, vinyl.year, vinyl.artists, vinyl.genres) not in vinyl_list:
                                    vinyl_list.add((vinyl.title, vinyl.year, vinyl.artists, vinyl.genres))
                                    ids.append(vinyl.id)
                                    print("n1")
                                    ok = True
                                    vinyl_graph.add((release_uri, RDF.type, mo.Vinyl))
                                    print("n2")
                                    vinyl_graph.add((release_uri, dc['title'], Literal(vinyl.title)))
                                    print("n3")
                                    if vinyl.year != 0:
                                        vinyl_graph.add((release_uri, dc['date'], Literal(vinyl.year)))
                                    print("n4")
                                    if vinyl.images:
                                        vinyl_graph.add((release_uri, mo['imageUrl'], Literal(vinyl.images[0]['uri'])))
                                    print("n5")
                        except Exception as e:
                            print(e)
                            print(8)
                        current_artists = []
                        try:
                            print("artists",vinyl.artists)
                            if vinyl.artists is not None and len(vinyl.artists) > 0:
                                current_artists = add_artists(vinyl, release_uri, ok)
                        except Exception as e:
                            print(e)
                            print(6)
                        try:
                            if vinyl.tracklist is not None and len(vinyl.tracklist) > 0:
                                add_songs(vinyl, release_uri, ok, current_artists)
                        except Exception as e:
                            print(e)
                            print(9)
                        try:
                            if vinyl.genres is not None:
                                add_genres(vinyl, release_uri, ok)
                        except Exception as e:
                            print(e)
                            print(10)

                        try:
                            if ok:
                                if vinyl.title != '' and vinyl.genres is not None and vinyl.tracklist is not None and vinyl.artists is not None:
                                    if (vinyl.title, vinyl.year, vinyl.artists, vinyl.genres) not in vinyl_list:
                                        ttl_data = vinyl_graph.serialize(format='turtle')
                                        with open('vinyl-3.ttl', 'a',encoding='utf-8') as ttl_file:
                                            ttl_file.write(ttl_data)
                        except Exception as e:
                            print(e)
                            print(71)

                    except UnicodeEncodeError as e:
                        print(e)
                        print(2)

                        continue
                    except Exception as e1:
                        print(e1)
                        print(3)

                        continue

            except discogs_client.exceptions.HTTPError as e:
                print(e)
                print(4)

                continue

    except Exception as e:
        print(e)
        print(5)


get_all_vinyl_releases()
