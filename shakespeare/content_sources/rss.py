import feedparser
import datetime as dt

#rss feed dictionary
rss_feeds = {
            'pnas':'http://www.pnas.org/rss/current.xml',
            'small':'http://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1613-6829',
            'advmat':'http://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1521-4095',
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
        today = dt.date.today()
        for entry in entries:
            article = dict()
            for kw,fkw in zip(['title','author','abstract','url'],['title','author','summary','link']):
               article[kw] = entry[fkw] if fkw in entry else ''
            #make sure this article is recent
            t_str=None
            if 'updated' in entry:
                t_str = entry['updated_parsed']
            elif 'published' in entry:
                t_str = entry['published_parsed']
            if t_str:
                day = t_str.tm_mday
                month = t_str.tm_mon
                year = t_str.tm_year
                pdate = dt.date(day=day,month=month,year=year)
                if (today-pdate).days<8:
                    articles.append(article)
            else:
                articles.append(article)

        return articles
