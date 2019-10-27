import HTMLParser
import re
parser = HTMLParser.HTMLParser()


def parse_index_page_info(html_str):
    found = re.findall("<h1[^>]+>([^<]+)?</h1>", html_str)
    title = found[1].decode('utf-8') if (len(found) > 1 and found[1]) else found[0].decode('utf-8')
    title = parser.unescape(title)
    print(title)
    found = re.findall('<a href="(([^"]+)-1)"', html_str)
    start_url = found[0][0]
    return start_url, title
