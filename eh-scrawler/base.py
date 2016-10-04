
import subprocess as sub

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


def mkdir_with_autocreate(dst):
    p = sub.Popen(['mkdir', '-p', dst], stdout=sub.PIPE,
                  stderr=sub.PIPE)
    output, errors = p.communicate()


def download_img(url, dst):
    print "download ", url
    ctnt = None
    for _ in xrange(5):
        print "_try ", _
        try:
            resp, ctnt = hc.request(url)
            if '200' == resp.get('status'):
                break
        except Exception as e:
            print "Download failed: ", e
            continue

    # print ctnt
    if ctnt is None:
        print "Failed img:", url
        return
    with open(dst, 'wb') as f:
        f.write(ctnt)


def cp(old, new):
    p = sub.Popen(['cp', old, new], stdout=sub.PIPE,
                  stderr=sub.PIPE)
    output, errors = p.communicate()