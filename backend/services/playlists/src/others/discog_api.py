import discogs_client

d = discogs_client.Client(
        'my_user_agent/1.0',
        consumer_key='FyoGoXsounPyHHaemfJB',
        consumer_secret='eOqnRHRjwLXWVASyKoalJYQagNWPFViy',
    )

d = discogs_client.Client('discog_user_agent/1.0')
d.set_consumer_key('FyoGoXsounPyHHaemfJB', 'eOqnRHRjwLXWVASyKoalJYQagNWPFViy')

def get_token():
    try:
        val = d.get_authorize_url('http://localhost:3000/profile')
        if len(val) == 3:
            return {
                "msg": "Discog token",
                "token": val[2]
                }
        else:
            return {
                "msg": "Could not get discog token"
            }, 400
    except Exception as e:
        print(e)
        return {
            "msg": "Could not get discog token"
        }, 400
    
def get_user_wantlist():
    try:
        me = d.identity()
        my_wantlist = me.wantlist

        tracks_response = []
        for i in range(0, my_wantlist.pages):
            for wantlist_item in (my_wantlist.page(i)):
                for artist in wantlist_item.release.artists:
                    for genre in wantlist_item.release.genres:
                        tracks_response.append({
                            "title": wantlist_item.release.title,
                            "date": wantlist_item.release.year,
                            "artist": artist.name,
                            "genre": genre
                        })
        
        return tracks_response

    except Exception as e:
        print(e)
        return []
       
def set_verifier(verifier):
    try:
        d.get_access_token(verifier)
        return get_user_wantlist()
    except Exception as e:
        print(e)
        return {
            "msg": "Could not get discog info"
        }, 400
