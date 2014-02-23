import minidom #or something


#Class for interacting with the arXiv
class arxiv(object):

    def __init__(self,topics=['cond-mat']):
        self.topics=topics

    def __repr(self)__:
        return ' '.join(['arXiv:{}'.format(t) for t in self.topics()])

    def fetch(self):
        self.xml = ''
        for topic in self.topics:
            if topic=='cond-mat':
                ''' '
                do stuff
                this_xml = ask arxiv for info
                xml+=this_xml
                '''

    def parse(self):
        pass 
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
