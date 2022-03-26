#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 11:26:21 2022

This is a data class we will use to represent a column of string data for string matching.

This class can either take in our data from a python object, or read it from a file on disk.

The data will be represented as a numpy array, and the class will implement critical string-cleaning funcitons.

As we clean, we keep a copy of the original data in self.originalData

@author: RobertTeresi
"""

# Import libraries and classes - dependencies for our StringColumn class
from tkinter.tix import ROW
import pandas as pd
import numpy as np

# This is probably the best class to use to split our strings into their component words for identifying stopwords.
from sklearn.feature_extraction.text import CountVectorizer

# This is Raja's preferred nlp library:
import nltk
from nltk.corpus import webtext
from nltk.probability import FreqDist

class StringColumn:
    
    # Initialization function for our class.
    def __init__(self, data=None, path=None, sep=","):
        '''
        
        Initialization function for our class.
        
        Must provide either an array-list object of our data, or provide a source to read in the data from.
        
        Parameters
        ----------
        data : Array-like object of strings, optional
            If creating the class from an existing python object.
                            Should be an array-like object full of strings. 
                            The default is None.
        path : Str, optional
            If creating the class from an object on disk. 
                            Should be a single column and will treat all entries as strings.
                            The default is None.
        
        sep : Str
            If reading data from .csv file, what to use as the separator.

        Returns
        -------
        StringColumn
            The initialized Key Column Class. 

        '''
        
        if data is not None:
            if type(data) is not np.ndarray:
                self._data = np.array(data)
            
            elif type(data) is np.ndarray:
                self._data = data
            
        elif path is not None:
            # Must be a string
            assert type(path) is str
            self._data = np.array(pd.read_csv(path).iloc[:,0])
        
        # Check that the data is one dimensional.
       
        if np.ndim(self._data) != 1:
            print("Input data is not one column.")
        else:
            print("Input data is one column wide. Ready to analyze.")
        
        # Check that each cell in the numpy array of the data is a string.
        # If it isn't, cast it as a string.

        for row in self._data:
            # to check initial type of each row in the numpy array
            # print(type(row))
            assert type(row) is str
            # to check final type of each row
            # print(type(row))
        
        # Save the originalData
        self._originalData = self._data
        self.potentialStopwords = None
        
    # How to access the class data
    def __getitem__(self,i):
        '''
        
        How our class is accessed.
        
        Parameters
        ----------
        i : integer
            Desired location in current data array.

        Returns
        -------
        String
            String of data at location i.

        '''
        
        return self._data[i]
    
    # What to return for the length of the class
    def __len__(self):
        """
        
        How length is calculated on our class.
        
        Returns
        -------
        integer. Return length of data array.

        """
        return len(self._data)

    def lower(self):
        '''
        
        Convert our data to lowercase.
        
        Returns
        -------
        None. Converts data to lowercase.
        '''

        for row in self._data:
            row = row.lower()
    
    def rm_punct(self, punc_list=None):
        '''
        
        Remove punctuation from our strings.

        Parameters
        ----------
        punct_list : list, optional
            If you only want to remove certain punctuation characters, enter in a list of them and only those characters will be removed.
            The default is None.

        Returns
        -------
        None. Removes punctuation from data.

        thanks to:
        https://www.geeksforgeeks.org/python-remove-punctuation-from-string/

        '''
        
        # default punctuation character list:
        punc_list = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        
        for row in self._data:
            # delete all the punctuation characters
            for ch in row:
                if ch in punc_list:
                    row = row.replace(ch, "")
        
    def identify_potential_stopwords(self, min_threshold=.1):
        """
        * From Raja: I like this idea! I'm using this resource to continue:
        * https://www.pythonprogramming.in/find-frequency-of-each-word-from-a-text-file-using-nltk.html

        Identifying "stopwords" in our string data. This will be an inductive method to discover parts of our string that
        may not be very informative. If a word appears in over the minimum threshold proportion of words, we identify it as a potential stopword.
        The thinking here is that common, potentially optional, words (like "inc" in a business context) may introduce too much noise for matching strings across datasets.

        Parameters
        ----------
        min_threshold : float, optional
            Must be between 0 and 1, obviously. What proportion of  The default is .1.

        Returns
        -------
        Update our class's potential stopwords variable. I am open to how this data is structured is eventually structured.
        I am imagining something like a list of tuples where the first item of the tuple is word, and second item is its proportion of strings it is found in. 
        
        The final result should be sorted with the most prevalent words first and the least prevalent (which are still above the threshold) last.

        """
        # Create one large string with the contents of the whole array.
        all_words = ''
        for row in self._data:
            all_words = all_words + ' ' + row

        # Create a frequency distribution of that string.
        data_analysis = nltk.FreqDist(all_words)

        # Let's take the specific words only if their frequency is greater than 3.
        # filter_words = dict([(m, n) for m, n in data_analysis.items() if len(m) > 3])
        
        print(data_analysis)

        '''
        for key in sorted(filter_words):
            print("%s: %s" % (key, filter_words[key]))
        
        data_analysis = nltk.FreqDist(filter_words)
        
        data_analysis.plot(25, cumulative=False)
        '''
    
    def remove_stopwords_fromlist(self, stopword_list):
        """
        
        This function removes stopwords that the user specifically names.

        Parameters
        ----------
        stopword_list : List-like object
            List of stopwords to remove from the strings before matching.

        Returns
        -------
        None. Removes stopwords from strings in our data object.

        """
        
        stopword_list = list(stopword_list) # this can be an array, or whatever, but have to convert it to whatever type you want to deal with first
        pass
    
    def remove_stopwords_automatically(self, use_avail_potential_stopwords=False, min_threshold=None):
        """
        
        This function removes stopwords by locating the most prevalent words in our strings and removing them without user supervision.

        Parameters
        ----------
        use_avail_potential_stopwords: bool
            If the user already identified potential stopwords, we will use them instead of running that step again.
            This will override the min_threshold function, making it meaningless.
        
        min_threshold : float, optional
            What threshold will be used to identify our potential stopwords.
            The default is None and means that we will use the default value in identify_potential_stopwords (=.1 right now) to identify stopwords that we remove.

        Returns
        -------
        None. Removes stopwords from strings in our data object.

        """
        pass
        
def main():
    print("Running main method.")
    sc = StringColumn(path='/Users/rajamoreno/Dropbox/som_work/FuzzyStringMatcher/SampleData/businessNameDirectory.csv')
    print(sc.__len__())
    # for i in range(sc.__len__()):
        # print(sc.__getitem__(i))
    print(sc)
    sc.lower()
    print(sc)
    sc.rm_punct()
    print(sc)
    sc.identify_potential_stopwords()

# This part of the script only runs if you are running this .py script, not if you are importing it to another file.
# This is the place to write tests for the class.
if __name__ == '__main__':
    main()