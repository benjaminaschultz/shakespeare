#!/usr/bin/env python
import re, glob, sys,os
import argparse
import itertools as it
import numpy as np
import scipy.sparse
import cPickle as pickle
from sklearn.naive_bayes import MultinomialNB
from content_sources import arxiv, bibtex, rss

def find_keywords(text):

    keywords=re.sub('[{}:?!@#$%^&*\(\)_.\\/,\'\"]','',text).upper()
    prepositions = open('data/prepositions.dat').read().upper().split()

    for p in prepositions:
        keywords = re.sub(r"\b{!s}\b".format(p),' ',keywords)

    return keywords.encode('ascii','ignore').split()

def test(argv):
    #train the algorithm
    #read in titles we like
    good_titles_kw = find_keywords(open('data/allTitles.dat').read())
    #read in titles we don't
    bad_titles_kw = find_keywords(open('data/arxivTitles.500.dat').read())

    #remore duplicate words
    good_kw_set = set(good_titles_kw)
    bad_kw_set = set(bad_titles_kw)

    #make a set of all the words
    all_kw_set = good_kw_set.union(bad_kw_set)


    #count the occurences of each of the the keywords
    good_freq = np.zeros(len(all_kw_set))
    bad_freq = np.zeros(len(all_kw_set))
    all_freq = np.zeros(len(all_kw_set))

    ##good_txt = ' '.join(good_titles_kw)
    ##bad_txt = ' '.join(bad_titles_kw)

    for i,kw in enumerate(all_kw_set):
        good_freq[i] += good_titles_kw.count(kw)# len(re.findall(r"\b{!s}\b".format(kw), good_txt))
        bad_freq[i] += bad_titles_kw.count(kw) # len(re.findall(r"\b{!s}\b".format(kw), bad_txt))

    all_freq = good_freq+bad_freq

    #compute the base rates of words in the good or bad set
    base_good = np.sum(good_freq)/np.sum(all_freq)
    base_bad = np.sum(bad_freq)/np.sum(all_freq)

    #compute the "evidence probabilites"
    evidence_prob = all_freq/np.sum(all_freq)

    #compute likelihood of word being good and bad
    good_likelihood  = good_freq/all_freq
    bad_likelihood  = bad_freq/all_freq

    #make a dictionary to easily access likelihoods of our keywords
    gl_dict = {kw:lh for kw,lh in zip(all_kw_set,good_likelihood)}
    bl_dict = {kw:lh for kw,lh in zip(all_kw_set,bad_likelihood)}

    #read in new titles
    new_titles = open('data/arxivTitles.feb20.300.dat').readlines()
    nt_good_scores = np.empty(len(new_titles))
    nt_bad_scores = np.empty(len(new_titles))

    #compute score for each new title
    for i,nt in enumerate(new_titles):
        nt_kw_set = set(find_keywords(nt))
        nt_good_scores[i] = base_good*np.prod([gl_dict[kw] for kw in nt_kw_set if kw in gl_dict])
        nt_bad_scores[i] = base_bad*np.prod([bl_dict[kw] for kw in nt_kw_set if kw in bl_dict])

    for b,g,t in zip(nt_bad_scores,nt_good_scores,new_titles):
        print(b,g,'GOOD!' if g>b and g>0 else 'BAD!',t)

#read existing knowledge from a database
def parse_knowledge(knowledge_db):
    pass

# \param nb = MultinomialNB classifier
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

def get_content(sources):
    all_content = list()
    for src in sources:
        try:
            src.fetch()
        except:
            print("Fetch of content from {!r} has failed".format(src))

        content = None
        try:
            content = src.parse()
        except:
            print("parsing of content from {!r} has failed".format(src))

        if content:
            all_content += content

    return all_content


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


#training suite
def train(good_sources, bad_sources,method,naive_bayes=None,keywords=list()):
    #train the algorithm
    good_samples = find_keywords(' '.join([entry[method] for entry in good_sources]))
    bad_samples = find_keywords(' '.join([entry[method] for entry in bad_sources]))


    #if we have an exists knowledge base to append this new information to, do so
    if naive_bayes:
        new_kws = set(good_samples+bad_samples).difference(keywords)

        #make some call to naive_bayes.partial_fit in here
        X = np.concatenate((naive_bayes.feature_count_, np.zeros((naive_bayes.feature_count_.shape[0],naive_bayes.feature_count_.shape[1]+len(new_kws)))),1)
        keywords += list(new_kws)

        all_kw = keywords + [nkw for nkw in new_kws if nkw not in keywords]

    else:
        all_kw = list(set(good_samples+bad_samples))
        X = np.zeros((2,len(all_kw)))

    for j,kw in enumerate(all_kw):
        X[0,j] += good_samples.count(kw)
        X[1,j] += bad_samples.count(kw)

    y = ['good','bad']

    naive_bayes = MultinomialNB()
    naive_bayes.fit(X,y)

    return naive_bayes, all_kw

def to_markdown(content,output_file):
    try:
         with open(output_file,'w') as outf:
            outf.write('# Relevant articles\n')
            for article in content:
                outf.write("## {}\n".format(article['title'].encode('ascii','ignore')))
                outf.write("* authors: {}\n".format(article['author'].encode('ascii','ignore')))
                outf.write("* abstract: {}\n".format(article['abstract'].encode('ascii','ignore')))
                outf.write("* [link]({})\n\n".format(article['url'].encode('ascii','ignore')))
    except:
        print("Failed to write markdown file")

def review_content(good_content,content,method,review_all=False):
    to_review=[]
    if review_all:
        to_review = content
    else:
        to_review = good_content

    human_class=[]
    for entry in to_review:
        print("Is \"{}\" a good entry?".format(entry[method]))
        decision = raw_input('Y/n?').lower()
        human_class.append('good' if decision=='y' else 'bad')
    return human_class, to_review

def main(argv):

    #add command line options for sources, output prefs, database of "good" keywords
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--output', help='output file name. only supports markdown right now.',dest ='output',default=None)
    parser.add_argument('-b','--bibtex', help='bibtex files to fetch',dest='bibfiles', nargs='*',default=list())
    parser.add_argument('-j','--journals', help='journals to fetch. Currently supports {}.'.format(' '.join(rss.rss_feeds.keys())),
                        nargs='*',dest='journals',default=list())
    parser.add_argument('-a','--arXiv', help='arXiv categories to fetch',
                      nargs='*',dest='arXiv',default=list())
    parser.add_argument('--all_sources', help='flag to search from all sources.',action ='store_true')
    parser.add_argument('--all_good_sources', help='flag to search from good sources. Specfied in your config file.',action ='store_true')
    parser.add_argument('--train', help='flag to train. All sources beside "--train-input-good" are treated as bad/irrelevant papers',action ='store_true')
    parser.add_argument('-g','--train_input_good', help='bibtex file containing relevant articles.',dest ='good_source',default=None)
    parser.add_argument('-m','--method', help='Methods to try to find relevent papers. Right now, only all, title, author, and abstract are valid fields',
                        dest='method',default='title')
    parser.add_argument('-k', '--knowledge',
                        help='path to database containing information about good and bad keywords. \
                              If you are training, you must specifiy this, as it will be where your output is written ',
                        dest='knowledge',default=None)
    parser.add_argument('--overwrite-knowledge', help='flag to overwrite knowledge,if training',action ='store_true',default=True, dest='overwrite_knowledge')
    parser.add_argument('--feedback', help='flag to give feedback after sorting content',action ='store_true',default=False, dest='feedback')
    parser.add_argument('--review_all', help='review all the new selections. Otherwise, you will only review the good selections',action ='store_true',default=False, dest='review_all')
    args = parser.parse_args(argv)

    if  not args.method in ['title','abstract','author, all']:
            print("Invalid method. Options are title, abstract, author, and all")
            exit()

    method = args.method

    #Set up training if that's what we're doing
    if args.train:

        #check to make sure we have a good training input
        if args.good_source is None:
            print("When training, you must specify one good source")
            exit()
        if not os.path.exists(args.good_source):
            print("Specified training input does not exist")
            exit()
        if not os.path.isfile(args.good_source):
            print("Specified training input is not a file")
            exit()
        if not os.path.splitext(args.good_source)[1] == '.bib' :
            print("Training input must be in bibtex format")
            exit()

        #load the existing knowledge
        nb,kw,knowledge = load_knowledge(args.knowledge)
        if args.overwrite_knowledge:
            nb=None
            kw=list()

        good_content = get_content([bibtex.BibTex(args.good_source)])

        if args.all_sources:
            bad_content = get_content([arxiv.ArXiv(cat) for cat in arxiv.arxiv_cats] +
                                      [rss.JournalFeed(journal) for journal in rss.rss_feeds.keys()])
        else:
            bad_content = get_content([arxiv.ArXiv(cat) for cat in args.arXiv] +
                                      [bibtex.BibTex(bibfile) for bibfile in args.bibfiles] +
                                      [rss.JournalFeed(journal) for journal in args.journals])

        #train, and write out knowledge (naive_bayes class and keywords)
        nb, kw = train(good_content,bad_content,method,naive_bayes=nb, keywords=kw)
        pickle.dump(nb,open(knowledge+'/nb.p','w'))
        pickle.dump(kw,open(knowledge+'/kw.p','w'))

    #we are filtering new content through our existing knowledge
    else:

        #load the old knowledge
        nb,kw,knowledge = load_knowledge(args.knowledge)
        if args.all_sources:
            sources = [arxiv.ArXiv(cat) for cat in arxiv.arxiv_cats] + \
                      [rss.JournalFeed(journal) for journal in rss.rss_feeds.keys()]
        else:
            sources = [arxiv.ArXiv(cat) for cat in args.arXiv] + \
                      [ bibtex.BibTex (bibfile) for bibfile in args.bibfiles] + \
                      [rss.JournalFeed(journal) for journal in args.journals]

        new_content = get_content(sources)

        good_content = filter_content(new_content,method,nb,kw)
        print("Fraction of good new content: {!r}".format(len(good_content)*1.0/len(new_content)))
        print("total  content parsed: {!r}".format(len(new_content)))

        if (args.output):
            to_markdown(good_content,args.output)
        else:
            pass
            #print(good_content)

        if(args.feedback):
            human_class, reviewed_content = review_content(good_content,new_content,method,args.review_all)
            good_content = [entry for cat,entry in zip(human_class,reviewed_content) if cat=='good']
            bad_content = [entry for cat,entry in zip(human_class,reviewed_content) if cat=='bad']
            nb, kw = train(good_content,bad_content,method,naive_bayes=nb, keywords=kw)
            pickle.dump(nb,open(knowledge+'/nb.p','w'))
            pickle.dump(kw,open(knowledge+'/kw.p','w'))




if __name__=="__main__":
    main(sys.argv[1:])
