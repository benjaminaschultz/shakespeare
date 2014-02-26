import re
import os
from bibtexparser.bparser import BibTexParser

#Parse Bibtex file and return dictionary
class BibTex(object):

    def __init__(self,filename):
        self.filename = filename

    def __repr__(self):
        return 'BibTex File {} '.format(self.filename)

    def fetch(self):
        if not os.path.exists(self.filename):
            raise Exception("Bibtex file {} does not exist".format(self.filename))
        if not os.path.isfile(self.filename):
            raise Exception("Bibtex file {} is not a file".format(self.filename))

    def parse(self):
        articles= list()
        with open(self.filename,'r') as bibfile:
            entries = BibTexParser(bibfile).get_entry_list()
            for entry in entries:
                article=dict()
                for kw,btpkw in zip(['title','author','abstract','url'],['title','author','abstract','link']):
                    article[kw]= entry[btpkw] if btpkw in entry else ''
                articles.append(article)
        return articles
