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
            s['cost'] = int(''.join(i.split('class="ui-s2')[1].split(' ₽</span>')[0].split('>')[-1].split()))
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
