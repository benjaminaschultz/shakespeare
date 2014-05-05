import sklearn as skl
import numpy as np
import pickle as p
import sys
sys.path.append('../')
import shakespeare as shake


def test_total_train():
    '''
    This test generates a bunch of words, constructs 'good' and 'bad'
    titles from them, and then uses shakespeare library calls to train
    a naive_bayes classifier.

    It then generates a second set of different titles using random
    combinations of the same good and bad words, and verifies that these
    titles are classified properly.
    '''
    letters = np.array(['{:c}'.format(i) for i in np.arange(65,65+26)])
    words = letters[np.random.uniform(0,26,size=(10000,15)).astype(np.int)]
    words = np.array([''.join(w) for w in words])

    #good titles contain words from 0-1000
    good_titles =  words[np.random.uniform(0,1000,size=(300,15)).astype(np.int)]
    good_titles = [{'title':' '.join(g)} for g in good_titles]

    #bad titles contain words from 800-4000; there are ~200 possible overlapping words.
    bad_titles =  words[np.random.uniform(800,4000,size=(300,15)).astype(np.int)]
    bad_titles = [{'title':' '.join(g)} for g in bad_titles]

    #train
    shk = skl.naive_bayes.MultinomialNB()
    nb,kw=shake.train(good_titles,bad_titles,'title')

    #generate new titles to verify that they will be properly classified
    test_good_titles =  words[np.random.uniform(0,1000,size=(100,15)).astype(np.int)]
    test_good_titles = [{'title':' '.join(g)} for g in test_good_titles]
    test_bad_titles =  words[np.random.uniform(800,4000,size=(100,15)).astype(np.int)]
    test_bad_titles = [{'title':' '.join(g)} for g in test_bad_titles]
    screened = shake.filter_content(test_good_titles+test_bad_titles,'title',nb,kw)

    num_bad_tot = np.sum([s in test_bad_titles for s in screened])
    num_good_tot= np.sum([s in test_good_titles for s in screened])

    assert(num_good_tot*1.0/len(test_good_titles)>0.95)
    assert(num_bad_tot*1.0/len(test_good_titles)<0.05)
test_total_train.priority=1
test_total_train.status="stable"
test_total_train.slow=True

def test_incremental_train():
    '''
    This test  is basically the same as above, but it breaks the training into
    two steps to test the correctness of shakespeares updating of an exisiting
    naive bayes classifier

    It trains on one set of good and bad titles, generated as before. Then that naive_bayes
    classifier and list of keywords (shakespeares "knowledge") are given addtional good and
    bad titles to train against.

    Finally, this twice-trained classifier is used to classify a third set of good and bad 
    titles, and verifies that this  nb object classifies the test titles the same as an nb
    classifier that was trained on both sets of input titles at once.
    '''
    letters = np.array(['{:c}'.format(i) for i in np.arange(65,65+26)])
    words = letters[np.random.uniform(0,26,size=(10000,15)).astype(np.int)]
    words = np.array([''.join(w) for w in words])
    good_titles =  words[np.random.uniform(0,1000,size=(300,15)).astype(np.int)]
    good_titles = [{'title':' '.join(g)} for g in good_titles]
    bad_titles =  words[np.random.uniform(800,4000,size=(300,15)).astype(np.int)]
    bad_titles = [{'title':' '.join(g)} for g in bad_titles]
    shk = skl.naive_bayes.MultinomialNB()
    nb,kw=shake.train(good_titles,bad_titles,'title')

    test_good_titles =  words[np.random.uniform(0,1000,size=(100,15)).astype(np.int)]
    test_good_titles = [{'title':' '.join(g)} for g in test_good_titles]
    test_bad_titles =  words[np.random.uniform(800,4000,size=(100,15)).astype(np.int)]
    test_bad_titles = [{'title':' '.join(g)} for g in test_bad_titles]

    new_good_titles =  words[np.random.uniform(5000,6000,size=(100,15)).astype(np.int)]
    new_good_titles = [{'title':' '.join(g)} for g in new_good_titles]
    new_bad_titles =  words[np.random.uniform(800,5200,size=(100,15)).astype(np.int)]
    new_bad_titles = [{'title':' '.join(g)} for g in new_bad_titles]
    rt_nb,rt_kw=shake.train(new_good_titles,new_bad_titles,'title',naive_bayes=nb,keywords=kw)
    rt_screened = shake.filter_content(test_good_titles+test_bad_titles,'title',rt_nb,rt_kw)

    hk = skl.naive_bayes.MultinomialNB()
    all_nb,all_kw=shake.train(good_titles+new_good_titles,bad_titles+new_bad_titles,'title')
    all_screened = shake.filter_content(test_good_titles+test_bad_titles,'title',all_nb,all_kw)


    #make sure both identified the small good sources
    good_check = np.all([s in all_screened for s in rt_screened])
    assert(good_check)

    #make sure no bad sources made it through
    bad_check =  not (np.any([s in test_bad_titles for s in rt_screened])
                       and np.any([s in test_bad_titles for s in all_screened]))
    assert(bad_check)
test_incremental_train.priority=1
test_incremental_train.status="stable"
test_incremental_train.slow=True

if __name__=="__main__":
    test_incremental_train()
