import sys,os
import re,glob
import numpy as np
import scipy.sparse
from sklearn.naive_bayes import MultinomialNB
import cPickle as pickle
import pkg_resources

from . import content_sources

#remove punctuation and prepositions from a string
def find_keywords(text):
    keywords=re.sub('[{}:?!@#$%^&*\(\)_.\\/,\'\"]','',text).upper()
    prepositions = pkg_resources.resource_stream('shakespeare','data/prepositions.dat').read().upper().split()

    for p in prepositions:
        keywords = re.sub(r"\b{!s}\b".format(p),' ',keywords)

    return keywords.encode('ascii','ignore').split()

#Identify good entries using naive_bayes object
def filter_content(content,
                   method,
                   naive_bayes,
                   keywords):

    new_samples = [find_keywords(entry[method]) for entry in content]

    #compute vector for each new entry
    X = scipy.sparse.lil_matrix((len(new_samples),len(keywords)))

    for j,kw in enumerate(keywords):
        for i,ns in enumerate(new_samples):
            X[i,j]=ns.count(kw)

    categories = naive_bayes.predict(X)
    return [e for c,e in zip(categories,content) if c =='good']

#Gather content from all sources (BibTex files, arXiv, journal RSS feeds, etc)
def get_content(sources):
    all_content = list()
    for src in sources:
        try:
            src.fetch()
        except:
            print("Fetch of content from {!r} has failed".format(src))

        content = None
        try:
            print('parsing {!r}'.format(src))
            content = src.parse()
        except:
            print("parsing of content from {!r} has failed".format(src))

        if content:
            all_content += content

    return all_content

#Human review of content classification
#You can review all the content, or just one that the nb classifier thought were good.
#Human input is used to train the NB classifier.
def review_content(good_content,content,method,review_all=False):
    to_review=[]
    if review_all:
        to_review = content
    else:
        to_review = good_content

    human_class=[]
    for entry in to_review:
        print("Is \"{}\" a good entry?".format(entry[method].encode('ascii','ignore')))
        decision = raw_input('Y/n?').lower()
        human_class.append('good' if decision=='y' else 'bad')
    return human_class, to_review

#Load in a trained naive_bayes object and keyword list
def load_knowledge(knowledge):
    #existing naive_bayes object and keyword list
    nb=None
    kw=list()
    if knowledge is not None:
        if not os.path.isdir(knowledge):
            print("Knowledge bust be a directory")
            exit()

        kfiles = glob.glob(knowledge+'/*')
        if not 'nb.p' in kfiles:
            print("Knowledge does not contain nb.p (pickled naive bayes object)")
            exit()
        if not 'kw.p' in kfiles:
            print("Knowledge does not contain kw.p (pickled keyword list)")
            exit()

    else:
        knowledge =os.path.expanduser('~/.shakespeare')

    if os.path.exists(knowledge):
        nb=pickle.load(open(knowledge+'/nb.p'))
        kw=pickle.load(open(knowledge+'/kw.p'))

    return(nb,kw, knowledge)

#Train naive_bayes object on a data set
def train(good_sources, bad_sources,method,naive_bayes=None,keywords=list()):
    """
    This trains a MultinomialNB classifier with a bag of good words and a
    bag of bad words. This requires a kinda goofy work around to use sklearn's
    MultivariateNB class. In particular, updating the classifier with new content
    that contains new keywords, I don't use sklearn's partial_fit.
    """
    #train the algorithm
    good_samples = find_keywords(' '.join([entry[method] for entry in good_sources]))
    bad_samples = find_keywords(' '.join([entry[method] for entry in bad_sources]))

    #if we have an exists knowledge base to append this new information to, do so
    if naive_bayes:
        new_kws = set(good_samples+bad_samples)
        print('Using old keywords as well')
        print("# old keywords = {}\n # new keywords = {}".format(len(keywords),len(new_kws)))
        new_kws = set(good_samples+bad_samples).difference(keywords)
        print("# fresh keywords = {}\n".format(len(new_kws)))

        #Instead of doing a partial fit here, i want to expand the list of keywords
        #naive_bayes.feature_count_[0] contains the counts of words in 'bad' entries
        #naive_bayes.feature_count_[1] contains the counts of words in 'good' entries
        #This grabs the frequencies of all the old keywords and puts them into X
        #the entries corresponding to the new keywords are 0s appended to X
        X = np.concatenate((naive_bayes.feature_count_, np.zeros((naive_bayes.feature_count_.shape[0],len(new_kws)))),1)
        all_kw = keywords + list(new_kws)
    else:
        print('Only using keyownrds from this content set')
        all_kw = list(set(good_samples+bad_samples))
        X = np.zeros((2,len(all_kw)))

    for j,kw in enumerate(all_kw):
        X[0,j] += bad_samples.count(kw)
        X[1,j] += good_samples.count(kw)

    y = ['bad','good']

    naive_bayes = MultinomialNB()
    naive_bayes.fit(X,y)

    return naive_bayes, all_kw

#export content to simple markdown format
def to_markdown(content,output_file):
    try:
         with open(output_file,'w') as outf:
            outf.write('# Relevant articles\n')
            for article in content:
                outf.write("## {}\n".format(re.sub(r'\n',' ',article['title']).encode('ascii','ignore')))
                outf.write("* authors: {}\n".format(re.sub(r'\n',' ',article['author']).encode('ascii','ignore')))
                outf.write("* abstract: {}\n".format(re.sub(r'\n',' ',article['abstract']).encode('ascii','ignore')))
                outf.write("* [link]({})\n\n".format(re.sub(r'\n',' ',article['url']).encode('ascii','ignore')))
    except:
        print("Failed to write markdown file")

