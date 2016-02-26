
# coding: utf-8

# # Markov Chain

# **Learning Objectives:** Learn how to build Markov Chains from n-grams and generate new sequences from the Markov Chains.

# In[1]:

import types
from itertools import islice
import random


# ## n-grams

# You can read about the background information related to n-grams [here](https://en.wikipedia.org/wiki/N-gram). Write a function, `build_ngrams`, that returns n-grams from an input sequene (iterator). Try to do this without concrete lists. The `islice` function may be helpful.

# In[2]:

def build_ngrams(itr, n=2):
    """Return the sequence of n-grams from the source iterator."""
    return zip(*[itr[i:] for i in range(n)])


# In[3]:

a = build_ngrams(range(10), n=2)
assert hasattr(a, '__iter__') and not isinstance(a, list)
al = list(a)
assert al == [(i,i+1) for i in range(9)]

b = build_ngrams(range(10), n=5)
assert hasattr(b, '__iter__') and not isinstance(b, list)
bl = list(b)
assert bl == [(i,i+1,i+2,i+3,i+4) for i in range(6)]

assert list(build_ngrams('one two three four five six seven'.split(' '), n=5)) ==     [('one','two','three','four','five'),
     ('two','three','four','five','six'),
     ('three','four','five','six','seven')]


# ## Markov chain

# You can read about the background of Markov Chains [here](https://en.wikipedia.org/wiki/Markov_chain). Write a function `build_chain`, that returns a Markov Chain for a sequence of n-grams. This function should return a `dict` with:
# 
# * The keys will be the source node in the Markov Chain, which is the first `n-1` elements in each n-gram, as a `tuple`.
# * The values will be a *list* of possible targets in the Markov Chain. As you find new values for a single key, you will need to append to the list.

# In[4]:

def build_chain(ngrams, chain=None):
    """Build a Markov chain out of an iterator of n-grams.
    
    Parameters
    ----------
    ngrams: list of n-tuples
        A list of n-grams as tuples, where the first n-1 elements are the source node
        in the Markov chain ahd the last element is the target node in the Markov chain.
    chain: dict or None
        An existing Markov chain to add ngrams to or None for a new chain.
    """
    # YOUR CODE HERE
    dict = chain or {}
    for gram in ngrams:
        key = gram[0:len(gram)-1]
        value = (list(gram))[len(gram)-1:]
        if key not in dict:
            dict[key]= value
        else:
            dict[key] += value        
    
    return dict


# In[5]:

random.seed(0)
seq1 = [random.randint(0,10) for i in range(200)]
chain = build_chain(build_ngrams(seq1, n=3))
seq2 = [random.randint(0,10) for i in range(200)]
chain = build_chain(build_ngrams(seq2, n=3), chain=chain)
assert chain[(0,0)]==[7, 10, 0, 3, 4]
assert chain[(4,2)]==[1, 3, 8, 3, 7, 1, 10, 2, 8]
assert len(chain.keys())==111


# Write a function, `generate_sequence`, that can generate new sequences of length `m` from a trained Markov Chain (in the `dict` format described above). For the initial part of the sequence, randomly choose one of the keys in the Markov Chain `dict`.

# In[6]:

import random

def generate_sequence(chain, m):
    """Generate a new sequence of length n from a Markov chain.
    
    Parameter
    ---------
    chain : dict
        A dict where the keys are the source node of the Markov chain steps and
        the values are a list of possible targets.
    m : int
        The length of the sequence to generate.
    """
    # YOUR CODE HERE
    seq = list(chain.keys())
    seq = seq[random.randint(0, len(seq)-1)]
    
    keyLen = len(seq)
    
    keySet = seq
    seq = list(seq)
    
    for n in range(m - keyLen):
        if keySet in chain:
            length = len(chain[keySet])
            seq.append(chain[keySet][random.randint(0, len(chain[keySet])-1)])
        keySet = keySet[1:] + tuple([seq[len(seq)-1]])
        
    return seq


# In[7]:

random.seed(0)
seq3 = [random.randint(0,10) for i in range(200)]
chain2 = build_chain(build_ngrams(seq1, n=3))
assert list(generate_sequence(chain2, 10))==[8, 0, 1, 8, 10, 6, 8, 4, 8, 9]
chain3 = build_chain(build_ngrams(seq1, n=5))
assert list(generate_sequence(chain3, 10))==[4, 1, 8, 5, 8, 3, 9, 8, 9, 4]


# ## Scrape the web to find lyrics

# For this part of the exercise, you will need to find lyrics from one of your favorite bands, and use the [requests](http://docs.python-requests.org/en/latest/) and [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) packages to scrape the lyrics from a website. Some guidance:
# 
# 1. The more songs the better (many dozens).
# 2. No hand downloading or editing of the files, you must do everything from code.
# 3. Save all of the lyrics in a single text file in this directory.
# 
# I provide an example here of doing this for all of U2's lyrics. You will have to modify this code significantly for the band of your choice.

# In[8]:

import requests
from bs4 import BeautifulSoup


# First get the page that has an index of all the lyrics and create a list of the URLs of those pages:

# In[9]:

def get_lyric_urls():
    index = requests.get("http://www.metrolyrics.com/system-of-a-down-lyrics.html") # System of a Down
#     index = requests.get("http://www.metrolyrics.com/taylor-swift-lyrics.html") # System of a Down
    
    soup = BeautifulSoup(index.text, 'html.parser')
    lyric_paths = [link.get('href') for link in  
                   soup.find_all('tbody')[0].find_all('a')]
    return lyric_paths


# In[10]:

lyric_urls = get_lyric_urls()


# Here is a function that takes the URL of a single lyric page and scrapes the actual lyric as text:

# In[11]:

def get_lyric(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    html_lyrics = soup.find_all('div', class_='lyrics-body')[0].find_all('p')
    html_lyrics = [l.getText() for l in html_lyrics]
    return '\n'.join(html_lyrics)


# This gets all of the lyrics. Note the `time.sleep(1.0)`. When scraping websites, it is often important to throttle your requests so as to not get banned from the website.

# In[12]:

import time

def get_all_lyrics(lyric_urls):
    for url in lyric_urls:
        time.sleep(1.0)
        yield get_lyric(url)


# In[13]:

lyrics = get_all_lyrics(lyric_urls)


# Now save all the lyrics to a text file:

# In[14]:

with open('all_soad_lyrics.txt', 'w') as f:
    for lyric in lyrics:
        f.write(lyric.replace('\r\n', '\n'))
        f.write('\n')


# Leave the following cell to grade your code for this section:

# In[15]:

assert True


# ## Generate new lyrics with the Markov chain

# Here is the fun part!

# In[16]:

import textwrap


# Here are some simple function for tokenizing the lyrics:

# In[17]:

from quicktoken import tokenize_lines, tokenize_line, files_to_lines


# Read in your lyric file, tokenize the text (no stop words!) and generate new song lyrics. Some things to think about:
# 
# * This will work best if you generate new lines of text of some finite length (10-30 words).
# * Use `textwrap.wrap` to format these lines and separate them using newlines.
# * To get interesting results, you may need to run it multiple times.

# In[18]:

# YOUR CODE HERE
def capitalizeI(line):
    for word in range(len(line)):
        if line[word] == 'i' or line[word][0:2] == 'i\'':
            line[word] = line[word][0].upper() + line[word][1:]
    return line

def stanza(line, i):
    if (i + 1) % 4 == 0:
        for l in range(len(line)):
            if l == len(line) - 1:
                line[l] += ".\n"
    return line
        
def generate_song():
    seqFile = list(tokenize_lines(files_to_lines(['all_soad_lyrics.txt'])))

    chainFile = build_chain(build_ngrams(seqFile, n=8))
    song = []
    for i in range(16):
        line = list(generate_sequence(chainFile, 8))

        line[0] = line[0][0:1].upper() + line[0][1:]  #first letter is uppercase
        line = capitalizeI(line)
        line = stanza(line, i)
    
        song.append(" ".join(line))

    return song


# In[19]:

# textwrap.wrap(song, 40)
print("\n".join(generate_song()))


# In[ ]:




# In[ ]:



