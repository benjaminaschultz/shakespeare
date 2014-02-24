import feedparser

#rss feed dictionary
rss_feeds = {
            'PNAS':'http://www.pnas.org/rss/current.xml',
            'Nature':'http://feeds.nature.com/nature/rss/current?format=xml'
            }
#Class for interacting with the arXiv
class JournalFeed(object):

    def __init__(self,journal):
        self.journal=journal

    def __repr__(self):
        return 'rss feed : {}'.format(self.journal)

    def fetch(self):
        self.address=rss_feeds[self.journal]

    # extract the relevant fields from the xml returned from our arXiv query
    def parse(self):

        articles = list()
        entries = feedparser.parse(self.address)['entries']

        for entry in entries:
            article = dict()
            for kw,fkw in zip(['title','author','abstract','url'],['title','author','summary','link']):
               article[kw] = entry[fkw] if fkw in entry else ''
            articles.append(article)

        return articles
