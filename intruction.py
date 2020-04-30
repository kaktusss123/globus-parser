from re import search, sub


inst = {
    "_start_url": [
        "http://www.globus.ru/catalog/sobstvennoe-proizvodstvo/?count=36",
        "http://www.globus.ru/catalog/molochnye-produkty-syr-yaytsa/?count=36",
        "http://www.globus.ru/catalog/myaso-ryba-kulinariya/?count=36",
        "http://www.globus.ru/catalog/ovoshchi-frukty-zelen/?count=36",
        "http://www.globus.ru/catalog/khleb-konditerskie-izdeliya/?count=36",
        "http://www.globus.ru/catalog/bakaleya/?count=36",
        "http://www.globus.ru/catalog/zamorozhennye-produkty/?count=36",
        "http://www.globus.ru/catalog/napitki/?count=36",
        "http://www.globus.ru/catalog/alkogol/?count=36",
        "http://www.globus.ru/catalog/detskie-tovary/detskoe-pitanie/?count=36"
    ],
    "_base": "http://www.globus.ru",
    "_retry": 50,
    "_headers": {
        "Cookie": "globus_hyper_id=79; globus_hyper_name=%D0%A9%D0%B5%D0%BB%D0%BA%D0%BE%D0%B2%D0%BE",
        'Host': 'www.globus.ru',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.96 YaBrowser/20.4.0.1461 Yowser/2.5 Yptp/1.23 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru,en;q=0.9'
    },
    "_tree": {
        "pagination": "//div[@class=\"navigation js-navigation\"]/b/following-sibling::a[1]/@href",
        "item": "//a[contains(@class, \"pim-list__item\")][not(contains(@class,  \"pim-list__item--hidden\"))]/@href"
    },
    "fields": {
        "name": {
            'path': 'normalize-space(//div[@class="catalog-detail__title"]/h1/text())',
            'type': str,
        },
        "price": {
            'path': "//div[@class='catalog-detail__item-price-actual ']/span//text()|//div[@class='catalog-detail__item-price-actual catalog-detail__item-price-actual--discount-color']/span//text()",
            'type': lambda x: ','.join(x)
        },
        "descriprion": {
            "path": "normalize-space(//div[@class=\"catalog-detail__tabs\"]/div[1]/p/text())",
            "type": lambda x: sub(r'\s+', ' ', x)
        },
        "type": {
            "path": "//div[@class='bread']/a",
            "type": lambda x: '/'.join(map(lambda y: y.xpath('.//text()')[0], x[2:]))
        },
        "image": {
            "path": "normalize-space(//div[@class=\"catalog-detail__header-image\"]/img/@src)",
            "type": lambda x: 'https://www.globus.ru' + x
        }
    }, 
    "table": {
        "home": '//div[@class="catalog-detail-table"]/div[@class="catalog-detail-table__position"]',
        "title": "./div[@class='catalog-detail-table__position-title']/span/text()",
        "value": "./div[@class='catalog-detail-table__position-content']/span/text()"
    }
}