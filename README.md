shakespeare
===========

Identify relevant scientific papers with simple machine learning techniques

Installation
===========
run:

```
python setup.py --user install
```

to install shakespeare in ~/.local.

This will install the shakespeare python library, and also a script `shakespeare` that handles training, content fetching and content filtering.

To install an example knowledge set, copy examples' contents to $HOME/.shakespeare

Depends on `bibtexparser`, `feedparser` `scikit-learn` packages, which can be installed via pip

    pip install --user bibtexparser scikit-learn feedparser



Features
========

* fetch functions for the following journals
    
    * Phys Rev A-X
    * PRL
    * PNAS
    * Nature + Nature:Stuff
    * Science
    * Small
    * ACS Nano, Nano Letters
    * Soft Matter
    * Langmuir
    * Angewandte Chemie
    * JCP, JCP B

* Fetch functions for arXiv
* support for BibTex Files
* Naive bayes training and classification

Usage
======

Train naive\_bayes algorithm

    shakespeare -g thegoodstuff.bib -b thebadstuff.bib --train

Find papers from nature nano and PNAS

    shakespeare -j natnano pnas -o cool_papers.md

Find papers from the arxiv cond-mat.soft and math, then review the algorithms selection

    shakespeare -a cond-mat.soft math --feedback


Help printout

    usage: shakespeare    [-h] [-o OUTPUT] [-b [BIBFILES [BIBFILES ...]]]
                          [-j [JOURNALS [JOURNALS ...]]] [-a [ARXIV [ARXIV ...]]]
                          [--all_sources] [--all_good_sources] [--train]
                          [-g GOOD_SOURCE] [-m METHOD] [-k KNOWLEDGE]
                           [--overwrite-knowledge] [--feedback] [--review_all]
    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            output file name. only supports markdown right now.
      -b [BIBFILES [BIBFILES ...]], --bibtex [BIBFILES [BIBFILES ...]]
                            bibtex files to fetch
      -j [JOURNALS [JOURNALS ...]], --journals [JOURNALS [JOURNALS ...]]
                            journals to fetch. Currently supports physreve
                            physrevd jchemphysb physreva physrevc pnas nature
                            jchemphys science natmat physrevb acsnano jphyschem
                            nanoletters natphys prl small angewantechemie langmuir
                            physrevx natnano.
      -a [ARXIV [ARXIV ...]], --arXiv [ARXIV [ARXIV ...]]
                            arXiv categories to fetch
      --all_sources         flag to search from all sources.
      --all_good_sources    flag to search from good sources. Specfied in your
                            config file.
      --train               flag to train. All sources beside "--train-input-good"
                            are treated as bad/irrelevant papers
      -g GOOD_SOURCE, --train_input_good GOOD_SOURCE
                            bibtex file containing relevant articles.
      -m METHOD, --method METHOD
                            Methods to try to find relevent papers. Right now,
                            only all, title, author, and abstract are valid fields
      -k KNOWLEDGE, --knowledge KNOWLEDGE
                            path to database containing information about good and
                            bad keywords. If you are training, you must specifiy
                            this, as it will be where your output is written
      --overwrite-knowledge
                            flag to overwrite knowledge,if training
      --feedback            flag to give feedback after sorting content
      --review_all          review all the new selections. Otherwise, you will
                             only review the good selections


TODO
======
* Add support for a config file for setting defaults (e.g., which journals for search for when using the `--all_good_sources` command
