#!/usr/bin/env python
import re, glob, sys
import argparse
import numpy as np

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
        print(b,g,'GOOD!' if g>b and g>0 else 'BAD!',t)


def find_new_content(sources):

    from src in sources:
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
            #machine learing beep boop
            relevant_content = [{'title':'This is a paper','authors':['James Joyce'], 'doi':'23452retdrwr'},
                                {'title':'This is a paper','authors':['Ezra Pound', 'Ernest Hemingway'], 'doi':'werwe','url':'http://www.zombo.com'}]
            return relevant_content

#training suite
def train(good_sources, bad sources):
    pass

def to_markdown(content):
    pass

def main(argv):

    #add command line options for sources, output prefs, database of "good" keywords
    #use argparse

    sources = [ArXiv(topics=['cond-mat']), BibTex('some_file.bib')]
    new_content = find_new_content(sources)
    #format new_content
    to_markdown(new_content)



if __name__=="__main__":
    main(sys.argv[1:])
