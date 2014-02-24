#!/usr/bin/env python
import re, glob, sys
import argparse
import numpy as np
from content_sources import arxiv, bibtex, rss

def find_keywords(text):

    keywords=re.sub('[{}:?!@#$%^&*\(\)_.\\/,\'\"]','',text).upper()
    prepositions = open('data/prepositions.dat').read().upper().split()

    for p in prepositions:
        keywords = re.sub(r"\b{!s}\b".format(p),' ',keywords)

    return keywords.split()

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
        print(b,g,'GOOD!' if g>b and g >0 else 'BAD!',t)

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

def filter_content(content,knowledge,method):

    #base rates of words in the good or bad set
    base_good = knowledge[method]['base_good']
    base_bad = knowledge[method]['base_bad']

    #likelihoods of our keywords
    gl_dict = knowledge[method]['good_likelihood']
    bl_dict = knowledge[method]['bad_likelihood']

    #new content
    new_entries = [entry[method]  for entry in content]
    nt_good_scores = np.empty(len(new_entries))
    nt_bad_scores = np.empty(len(new_entries))

    #compute score for each new title
    for i,nt in enumerate(new_entries):
        nt_kw_set = set(find_keywords(nt))
        nt_good_scores[i] = base_good*np.prod([gl_dict[kw] for kw in nt_kw_set if kw in gl_dict])
        nt_bad_scores[i] = base_bad*np.prod([bl_dict[kw] for kw in nt_kw_set if kw in bl_dict])

    for b,g,t in zip(nt_bad_scores,nt_good_scores,content):
        if g>b and g >0:
            relevent_content.append(c)

    return relevant_content

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

#training suite
def train(good_sources, bad_sources):
    pass

def to_markdown(content):
    pass

def main(argv):

    #add command line options for sources, output prefs, database of "good" keywords
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--bibtex', help='bibtex files to fetch',dest='bibfiles', nargs='*',default=list())
    parser.add_argument('-j','--journals', help='journals to fetch. Currently supports {}.'.format(' '.join(rss.rss_feeds.keys())),
                        nargs='*',dest='titles',default=list())
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
        if not os.path.exist(args.good_source):
            print("Specified training input does not exist")
            exit()
        if not os.path.isfile(args.good_source):
            print("Specified training input is not a file")
            exit()
        if not os.path.splitext(args.good_source)[1] == '.bib' :
            print("Training input must be in bibtex format")
            exit()

        #make sure you have a good destination to write your training output
        if not os.path.exist(args.knowledge):
            print("Overwriting existings knowledege database")
            exit()
        if not os.path.isfile(args.knowledge):
            print("Specified training output exists and is not a file")
            exit()
        if not os.path.splitext(args.knowledge)[1] == '.dat' :
            print("Training output must be a dat file")
            exit()

        good_content = get_content([BibTex(args.good_source)])

        bad_content = get_content([arxiv.ArXiv(cat) for cat in args.arXiv] +
                                  [bibtex.BibTex(bibfile) for bibfile in args.bibfiles] +
                                  [rss.JournalFeed(journal) for j in journal])

    #we are filtering new content through our existing knowledge
    else:

        #locate our knowledge
        if (args.knowledge is None):
            pass

        knowledge = parse_knowledge()

        sources = [arxiv.ArXiv(cat) for cat in args.arXiv] + \
                  [bibtex.BibTex (bibfile) for bibfile in args.bibfiles] + \
                  [rss.JournalFeed(journal) for j in journal]
        new_content = get_content(sources)

        relevant_content = filter_content(content,knowledge,method)

        to_markdown(new_content)



if __name__=="__main__":
    main(sys.argv[1:])
