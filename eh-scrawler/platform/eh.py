
import re


def parse_index_page_html(html_str):
    found = re.findall("<h1[^>]+>([^<]+)?</h1>", html_str)
    print(found)
    title = found[1].decode('utf-8') if (len(found) > 1 and found[1]) else found[0].decode('utf-8')
    found = re.findall('<a href="(([^"]+)-1)"', html_str)
    start_url = found[0][0]
    return start_url, title
