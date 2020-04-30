import asyncio
from aiohttp import ClientSession, ClientTimeout, BasicAuth, TCPConnector
from lxml.html import fromstring as fs
import pandas as pd
from random import choice
from json import dumps
from datetime import datetime

from get_proxy import get_proxy
from intruction import inst

lock = asyncio.Lock()
auth = BasicAuth('komarik200026', 'T3b0JfY')

# def get_proxy():
#     '''Получить свежие прокси Натана'''
#     import requests
#     proxy_url = 'http://10.199.13.39:8085/get_data'
#     proxy_lim = 100
#     proxy_offset = 86500
#     json = {}
#     json['topic'] = 'proxies'
#     json['time_offset'] = proxy_offset
#     json['amount'] = proxy_lim
#     json['filter'] = ['schema', ['https']]
#     resp = requests.post(proxy_url, json=json).json()
#     resp = list(map(lambda x: x.get('value', {}).get(
#         'proxy', '').replace('https', 'http'), resp))
#     return resp

with open('proxy') as f:
    proxies = f.read().split()
# proxies = get_proxy()
print('Launching...')
print(proxies)


async def crawl(page_links: asyncio.Queue, item_links: asyncio.Queue, sess: ClientSession, prox: str):
    start = None
    while True:
        if start is None:
            start = await page_links.get()
        if not start.startswith('http'):
            start = inst['_base'] + start
        for tr in range(inst['_retry']):
            try:
                await asyncio.sleep(1.5)
                print(f'{start}    {tr}')
                async with sess.get(start, headers=inst['_headers'], proxy=prox, proxy_auth=auth, ssl=False) as resp:
                    page = fs(await resp.text())
                    items = page.xpath(inst['_tree']['item'])
                    for i in items:
                        await item_links.put(i)
                    nxt = page.xpath(inst['_tree']['pagination'])
                    start = nxt[0] if nxt else None
                    break
            except Exception as e:
                print(f'{e.__class__.__name__}: {e}')
                continue


async def parse(item_links: asyncio.Queue, sess: ClientSession, items: asyncio.Queue, prox: str):
    start = True
    while not item_links.empty() or start:
        start = False
        item = inst['_base'] + await item_links.get()
        for _ in range(inst['_retry']):
            await asyncio.sleep(1.5)
            try:
                async with sess.get(item, headers=inst['_headers'], proxy=prox, proxy_auth=auth) as resp:
                    txt = await resp.text()
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
                        await item_links.put(item[len(inst['_base']):])
                    else:
                        print(datetime.now())
                        await items.put(res)
                        break
            except:
                await item_links.put(item[len(inst['_base']):])
                continue


async def write(items: asyncio.Queue):
    open('res.txt', 'w').close()
    while 1:
        with open('res.txt', 'a', encoding='utf-8') as f:
            f.write(dumps(await items.get(), ensure_ascii=False) + '\n')


async def main():
    item_links = asyncio.Queue()
    items = asyncio.Queue()
    page_links = asyncio.Queue()
    for i in inst['_start_url']:
        await page_links.put(i)

    async with ClientSession(timeout=ClientTimeout(total=10), connector=TCPConnector(ssl=False)) as sess:
        futures = [asyncio.ensure_future(
            crawl(page_links, item_links, sess, prox)) for prox in proxies]
        futures += [asyncio.ensure_future(parse(item_links, sess, items, prox))
                    for prox in proxies]
        futures += [asyncio.ensure_future(write(items))]
        await asyncio.wait(futures)

if __name__ == '__main__':
    asyncio.run(main())
    # TODO: переделать все под синхронный реквест и сделать многопоточно
