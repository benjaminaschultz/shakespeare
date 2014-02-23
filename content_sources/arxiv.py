from xml.dom.minidom  import parseString
import urllib2

#Class for interacting with the arXiv
class arxiv(object):

    def __init__(self,topic='cond-mat'):
        self.topic=topic
        self.url_base = 'http://export.arxiv.org/api/'

    def __repr(self)__:
        return ' '.join(['arXiv:{}'.format(t) for t in self.topics()])

    def fetch(self):
        self.xml = ''
        query = 'query?search_query=cat:{}&start=0&max_results=100'.format(topic)
        self.xml = urllib2.urlopen(self.url_base + query).read()

    def parse(self):

        '''
        articles = list()
        for entry in self.xml:
            article = dict()
            for field in entry:
                 if field_name == 'title':
                    article['title'] = field_value
                if field_name == 'authoer':
                    article['title'] = authors
        .
        .
        .
        return articles
        '''
