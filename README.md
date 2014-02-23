shakespeare
===========

Identify relevant scientific papers with simple machine learning techniques

Installation
===========
Copy shakespeare.py to your pythonpath.

*Once we complete the script, we may consider putting most of the functionality into a library with a python API. Use CMake for an istaller*


Roadmap
========

* Add markdown output of relevant papers
* Add fetch functions for potentially relevent papers
    
    * Phys Rev A-Z
    * PRL
    * PNAS
    * Nature + Nature:Stuff
    * Science
    * Small
    * ACS Nano, Nano Letters
    * JACS
    * Soft Matter
    * Langmuir
    * Angewandte Chemie
    * JPC A,B,C, Letters
    * Macromolecules
    * Google Scholar email bot?

* Add fetch function for a bunch of other scientific journals (life sciences, etc) to train negative classification
* Training suite
    
    * The idea here is to have users import a mendeley library (maybe bibtex is best input) and then train against a diverse set of scientific journal

* Use distance package to identify close words
* Migrate our naive bayes implementation to [scikit-learn](http://scikit-learn.org/stable/user_guide.html).
* Migrate to SQL database instead of dat files? Probably easiest to keep this in mind as long term possibility if dat breaks. pandas seems like it might be useful for this task.
