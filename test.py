import urllib.request
from urllib.parse import urlparse
import requests


class Ozon_items():
    def __init__(self, url):
        request = urllib.request.urlopen(url).read().decode('utf-8')
        self.lib = []
        a = request.split('<body>')
        a = a[1]
        a = a.split('class="widget-search-result-container ')[1]
        a = a.split('</div></div></div></div><!---->')
        a = '><!----> '.join(a[0].split('><!----> ')[1:])
        a = a.split('</div><!----> ')
        id = 0
        for i in a:
            s = {}
            s[id] = id
            s['link'] = 'https://www.ozon.ru' + i.split('href="')[1].split(' class=')[0]
            #print(s['link'])
            s['img'] = i.split('<img src="')[1].split('" srcset=')[0]
            s['cost'] = int(''.join(i.split('class="ui-r6')[1].split(' ₽</span>')[0].split('>')[-1].split()))
            s['name'] = i.split('style="color:;"')[1].split('<span>')[1].split('</span>')[0]
            if len(s['name']) > 40:
                s['name'] = s['name'][:40] + '...'
            o = s['name']
            o = o.replace('&#34;', '"')
            o = o.replace('&#x2f;', "p")
            s['name'] = o
            s['cost'] = int(s['cost'])
            id += 1
            self.lib.append(s)


class Wild_items():
    def __init__(self, url):
        request = urllib.request.urlopen(urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'})).read().decode('utf-8')
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(request)


Wild_items('https://www.citilink.ru/search/?text=laptop')