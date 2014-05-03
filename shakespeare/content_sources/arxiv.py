from xml.dom.minidom  import parseString
import urllib2
import datetime as dt
arxiv_cats = ['astro-ph',
              'cond-mat',
              'gr-gc',
              'hep-ex',
              'hep-lat',
              'hep-ph',
              'hep-th',
              'math-ph',
              'nlin',
              'nucl-ex',
              'nucl-th',
              'physics',
              'quant-ph',
              'math',
              'CoRR',
              'q-bio',
              'q-fin',
              'stat']
#Class for interacting with the arXiv
class ArXiv(object):

    def __init__(self,topic='cond-mat'):
        self.topic=topic
        self.url_base = 'http://export.arxiv.org/api/'

    def __repr__(self):
        return 'arXiv:{}'.format(self.topic)

    def fetch(self):
        today=dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        end_date = "{:04d}{:02d}{:02d}2359".format(today.year,today.month,today.day)
        start_date = "{:04d}{:02d}{:02d}0000".format(week_ago.year,week_ago.month,week_ago.day)
        self.xml = ''
        query = 'query?search_query=cat:{}*+AND+submittedDate:[{}+TO+{}]&max_results=100'.format(self.topic,start_date,end_date)
        self.xml = urllib2.urlopen(self.url_base + query).read()

    # extract the relevant fields from the xml returned from our arXiv query
    def parse(self):

        articles = list()
        entries = parseString(self.xml).getElementsByTagName('entry')

        for entry in entries:
            article = dict()
            article['abstract'] = entry.getElementsByTagName('summary')[0].toxml().replace('<summary>','').replace('</summary>','')

            authors =list()
            for author in  entry.getElementsByTagName('author'):
                name = entry.getElementsByTagName('name')[0]
                authors.append(author.toxml().replace('<name>','').replace('</name>',''))

            article['author']= ', '.join(authors)

            article['title'] = entry.getElementsByTagName('title')[0].toxml().replace('<title>','').replace('</title>','')
            article['url'] = entry.getElementsByTagName('id')[0].toxml().replace('<id>','').replace('</id>','')

            articles.append(article)

        return articles
