WTF_CSRF_ENABLED = True
SECRET_KEY = b'\x1c<d\xa4\xaev\x93\x93\x060~\x15 \x9f\xaf\x1bo\x87\x17\xb6\\*\xafy'
TEMPLATES_AUTO_RELOAD = True
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]