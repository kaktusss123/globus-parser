from requests import get
from lxml.html import fromstring as fs
from threading import Thread
from queue import Queue
from datetime import datetime
from time import sleep
from json import dumps

from intruction import inst


with open('proxy', 'r') as f:
    proxies = f.read().split()

def crawl(page_links: Queue, item_links: Queue, prox: str):
    start = None
    while 1:
        if page_links.empty():
            return
        if start is None:
            start = page_links.get()
        if not start.startswith('http'):
            start = inst['_base'] + start
        for tr in range(inst['_retry']):
            try:
                sleep(2)
                print(f'{start}    {tr+1}')
                txt = get(start, proxies={'https': prox}, headers=inst['_headers'], timeout=30).text
                page = fs(txt)
                items = page.xpath(inst['_tree']['item'])
                for i in items:
                    item_links.put(i)
                nxt = page.xpath(inst['_tree']['pagination'])
                start = nxt[0] if nxt else None
                break
            except Exception as e:
                print(f'{e.__class__.__name__}: {e}')
                continue

def parse(item_links: Queue, items: Queue, prox: str):
    start = True
    while not item_links.empty() or start:
        start = False
        item = inst['_base'] + item_links.get()
        for _ in range(inst['_retry']):
            sleep(2)
            try:
                txt = get(item, headers=inst['_headers'], proxies={'https': prox}, timeout=30).text
                page = fs(txt)
                res = {'url': item}
                for k, v in inst['fields'].items():
                    val = page.xpath(v['path'])
                    res[k] = v['type'](val) if val else None
                table = page.xpath(inst['table']['home'])
                for t in table:
                    for k, v in zip(t.xpath(inst['table']['title']), t.xpath(inst['table']['value'])):
                        res[k] = v

                if res['name'] is None:
                    continue
                else:
                    print(datetime.now())
                    items.put(res)
                    break
            except Exception as e:
                print(f'{e.__class__.__name__}: {e}')
                continue


def write(items: Queue):
    open('res.txt', 'w').close()
    while 1:
        with open('res.txt', 'a', encoding='utf-8') as f:
            f.write(dumps(items.get(), ensure_ascii = False) + '\n')

if __name__ == '__main__':
    item_links = Queue()
    items = Queue()
    page_links = Queue()
    for i in inst['_start_url']:
        page_links.put(i)
    threads = [Thread(target=crawl, args=(page_links, item_links, prox)) for prox in proxies[:3]]
    threads += [Thread(target=parse, args=(item_links, items, prox)) for prox in proxies[3:]]
    threads += [Thread(target=write, args=(items,))]
    for t in threads:
        t.start()

    # 11:12