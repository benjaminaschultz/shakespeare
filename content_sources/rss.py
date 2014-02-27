import feedparser

#rss feed dictionary
rss_feeds = {
            'PNAS':'http://www.pnas.org/rss/current.xml',
            'Small':'http://onlinelibrary.wiley.com/rss/journal/10.1002/%28ISSN%291613-6829',
            'Nature':'http://feeds.nature.com/nature/rss/current?format=xml',
            'Science':'https://www.sciencemag.org/rss/current.xml',
            'PRL':'http://feeds.aps.org/rss/recent/prl.xml',
            'PhysRevA':'http://feeds.aps.org/rss/recent/pra.xml',
            'PhysRevB':'http://feeds.aps.org/rss/recent/prb.xml',
            'PhysRevB':'http://feeds.aps.org/rss/recent/prb.xml',
            'PhysRevC':'http://feeds.aps.org/rss/recent/prc.xml',
            'PhysRevD':'http://feeds.aps.org/rss/recent/prd.xml',
            'PhysRevE':'http://feeds.aps.org/rss/recent/pre.xml',
            'PhysRevX':'http://feeds.aps.org/rss/recent/prx.xml',
            'ACSNano':'http://feeds.feedburner.com/acs/ancac3',
            'NanoLetters':'http://feeds.feedburner.com/acs/nalefd',
            'JChemPhys':'http://phys.org/rss-feed/journals/journal-of-chemical-physics/',
            'JChemPhysB':'http://feeds.feedburner.com/acs/jpcbfk',
            'AngewanteChemie':'http://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1521-3773',
            'JPhysChem':'http://academic.research.microsoft.com/Rss?id=15120&cata=6',
            'NatPhys':'http://feeds.nature.com/nphys/rss/current',
            'NatMat':'http://feeds.nature.com/nmat/rss/current',
            'NatNano':'http://feeds.nature.com/nnano/rss/current',
            'Langmuir':'http://feeds.feedburner.com/acs/langd5'
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
