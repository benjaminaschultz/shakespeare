import re

#Parse Bibtex file and return dictionary
class BibTex(object):

    def __init__(self):
        pass

    def fetch(self, filename):
        return open(filename)

    def parse(filename):
        pass
        '''
        articles = list()
        for entry in filename:
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
