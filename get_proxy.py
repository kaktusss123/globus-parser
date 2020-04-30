from lxml.html import fromstring as fs
from requests import get

def get_proxy():
    page = fs(get('http://online-proxy.ru/index.html?sort=uptime').text)
    ip = page.xpath('//p[text()="Список бесплатных прокси"]/following-sibling::table//tr/td[2]/text()')
    port = page.xpath('//p[text()="Список бесплатных прокси"]/following-sibling::table//tr/td[3]/text()')
    return list(map(lambda x: 'http://' + ':'.join(x), zip(ip, port)))[:100]

