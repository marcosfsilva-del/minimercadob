import urllib.request, urllib.error
url='http://127.0.0.1:3001/cart'
try:
    r=urllib.request.urlopen(url)
    print('STATUS', r.getcode())
    print(r.read().decode()[:2000])
except urllib.error.HTTPError as e:
    print('HTTP', e.code)
    print(e.read().decode()[:2000])
except Exception as e:
    print('ERR', e)
