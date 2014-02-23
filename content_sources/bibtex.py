import re

#Parse Bibtex file and return dictionary
class BibTex(object):

    def __init__(self,filename):
        self.filename = filename

    def __repr__(self):
        return 'BibTex File {} '.format(self.file)

    def fetch(self):
        self.content = open(filename)

    def parse(filename):
        pass
        '''
        articles = list()
        for entry in self.content:
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
