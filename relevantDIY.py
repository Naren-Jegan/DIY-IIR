import requests
from bs4 import BeautifulSoup as bs
import pickle

pages = []
baseurl = 'https://www.google.co.in/search?q=DIY+%3A+Do+It+Yourself&oq=DIY+%3A+Do+It+Yourself&aqs=chrome..69i57.18399j0j8&sourceid=chrome&ie=UTF-8'
basecode = requests.get(baseurl)
baseplain = basecode.text
basehtml = bs(baseplain, "html.parser")
print(basehtml)
input()
for h3s in basehtml.find_all("h3", class_="r"):
    print('h3: ' + str(h3s))
    # input()
    baselink = h3s.find('a')
    if baselink is None:
        continue
    basepath = baselink.get('href')

    pages.append(basepath[7:])

print(pages)
input()

seen = False
relevant = []


def web_crawl(pages):
    count = 0
    iteration = 0
    while len(pages) is not 0:
        url = pages.pop(0)
        print('parsing: ' + str(url))
        hmtl = ""
        try:
            html = bs(requests.get(url).text, "html.parser")
        except KeyboardInterrupt:
            exit(0)
        except:
            continue
        content = ''.join(['%s' % x.text.lower() for x in html.find_all('p')])
        if any([x in content for x in ["do it yourself", "how to", "do yourself", "easy way", "ways to", "diy"]]):
            if url not in relevant:
                relevant.append(url)
            else:
                continue
            count += 1
            pages += [link.get('href')
                      for link in html.findAll('a')
                      if link.get('href') is not None and
                      link.get('href') not in relevant and
                      link.get('href') not in pages and
                      'https://' in link.get('href')
                      ]
        if count < 100:
            continue
        with open("./relevant.txt", 'a+') as f:
            f.write('\n'.join(relevant[iteration*100 : (iteration+1)*100]) + '\n')
        count = 0
        iteration += 1


web_crawl(pages)
