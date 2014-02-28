import feedparser

#rss feed dictionary
rss_feeds = {
            'pnas':'http://www.pnas.org/rss/current.xml',
            'small':'http://onlinelibrary.wiley.com/rss/journal/10.1002/%28issn%291613-6829',
            'nature':'http://feeds.nature.com/nature/rss/current?format=xml',
            'science':'https://www.sciencemag.org/rss/current.xml',
            'prl':'http://feeds.aps.org/rss/recent/prl.xml',
            'physreva':'http://feeds.aps.org/rss/recent/pra.xml',
            'physrevb':'http://feeds.aps.org/rss/recent/prb.xml',
            'physrevc':'http://feeds.aps.org/rss/recent/prc.xml',
            'physrevd':'http://feeds.aps.org/rss/recent/prd.xml',
            'physreve':'http://feeds.aps.org/rss/recent/pre.xml',
            'physrevx':'http://feeds.aps.org/rss/recent/prx.xml',
            'acsnano':'http://feeds.feedburner.com/acs/ancac3',
            'nanoletters':'http://feeds.feedburner.com/acs/nalefd',
            'jchemphys':'http://phys.org/rss-feed/journals/journal-of-chemical-physics/',
            'jchemphysb':'http://feeds.feedburner.com/acs/jpcbfk',
            'angewantechemie':'http://onlinelibrary.wiley.com/rss/journal/10.1002/%28ISSN%291521-3773',
            'jphyschem':'http://academic.research.microsoft.com/rss?id=15120&cata=6',
            'natphys':'http://feeds.nature.com/nphys/rss/current',
            'natmat':'http://feeds.nature.com/nmat/rss/current',
            'natnano':'http://feeds.nature.com/nnano/rss/current?format=xml',
            'langmuir':'http://feeds.feedburner.com/acs/langd5'
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
