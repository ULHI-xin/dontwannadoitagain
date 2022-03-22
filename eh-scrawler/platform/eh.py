
from html import unescape
from html.parser import HTMLParser
import re
parser = HTMLParser()


def parse_index_page_info(html_str):
    found = re.findall("<h1[^>]+>([^<]+)?</h1>", html_str)
    title = found[1] if (len(found) > 1 and found[1]) else found[0]
    # title = parser.unescape(title).replace('/', '_')
    title = unescape(title).replace('/', '_')
    print(title)
    found = re.findall('<a href="(([^"]+)-1)"', html_str)
    start_url = found[0][0]
    return start_url, title
