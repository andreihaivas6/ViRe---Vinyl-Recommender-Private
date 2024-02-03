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
            print(val[2])
            return {
                "msg": "Discog token",
                "token": val[2]}
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

        for i in range(0, my_wantlist.pages):
            for wantlist_item in (my_wantlist.page(i)):
                print(dir(wantlist_item))
                print(wantlist_item.release.title)
                print(wantlist_item.release.year)
                print(wantlist_item.release.artists[0].name)
                print(wantlist_item.release.genres)

    except Exception as e:
        print(e)
       
def set_verifier(verifier):
    try:
        d.get_access_token(verifier)
        get_user_wantlist()
        return {
            "msg": "Succeded",
        }
    except Exception as e:
        print(e)
        return {
            "msg": "Could not get discog info"
        }, 400
