

from httplib2 import Http

h = Http()
hc = Http('.cache')

def html_from_url(url, cookie):
    print "visit url", url
    for _ in xrange(10):
        print "_try ", _
        try:
            headers = {'Set-Cookie': cookie}
            resp, ctnt = h.request(url, headers=headers)
            if '200' == resp.get('status'):
                return ctnt, resp['set-cookie']
        except:
            continue