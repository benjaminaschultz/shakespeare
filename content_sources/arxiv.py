import minidom #or something


#Class for interacting with the arXiv
class arxiv(object):

    def __init__(self):
        pass

    def fetch(self,topics=['cond-mat']):
        xml = open('.arxiv.xml')
        for topic in topic:
            if topic=='cond-mat':
                ''''
                do stuff
                this_xml = ask arxiv for info
                xml.write(this_xml)
                '''
        xml.close()
        return 'arxiv.xml'

    def parse(self, filename):
        pass 
        '''
        articles = list()
        for entry in filename:
            a rticle = dict()
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
