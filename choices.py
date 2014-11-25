#  Copyright 2012 Tim McNamara

#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
choices is designed to make it easy to make it easy to 
make things happen in a probabilistic manner. Its main
API is the Choice class.

When called, a Choice object will return one of its keys
according to the proability it has been assigned.

Here's an example:

    >>> mood = Choice({'happy': 0.3, 'neutral': 0.6, 'sad': 0.1})
    >>> mood()
    'happy'
    >>> mood()
    'neutral'
    >>> mood()
    'neutral'


Creating a Choice object
========================

There are three main ways for creating a Choice object:

- a dict of keys and probabilities
- a list of (key, probability) pairs
- a list of (key, sample_count) pairs

Each of those options is explained below.

A dict of keys and probabilities
--------------------------------

Perhaps the simplest way to create a Choice is to
provide the keys and associated probability wrapped
up as a dict:

    >>> mood = Choice({'happy': 0.3, 'neutral': 0.6, 'sad': 0.1})
    >>> mood()
    'happy'
    >>> mood()
    'neutral'

A list of (key, probability) pairs
----------------------------------

As well as a dict assigning a probability to each key, you can
send in a list of (key,value) pairs as lists or tuples. This 
allows for lots of flexibility, including non-hashable
types to be used. This means that you can provide objects such 
as functions to be used as keys.

Let's say we wanted to create an NPC for a game and wanted
some scripted responses. Why not encode moods as functions
and then pass them togetheer as a Choice. 

  >>> def grumpy(news):
  ...    return ':/'
  >>> def happy(news):
  ...    return ':)'
  >>> react = Choice([(grumpy, 0.7), (happy, 0.3)])
  >>> reaction = react()
  >>> reaction("We're getting married!")
  ':/'

a list of (key, sample_count) pairs
-----------------------------------

You are not restricted to adding p to 1. If you only have samples,
and wish to calculate a probablilty distribution, you can provide 
those too:

   >>> birds_spotted = {'geese': 0, 'ducks': 12, 'sparrows': 4, 'other': 39}
   >>> birds = Choice(birds_spotted)
   >>> birds.distribution
   [('geese', 0.0), ('sparrows', 0.07272727272727272), ('ducks', 0.21818181818181817), ('other', 0.7090909090909091)]


Usage
=====

Making decisions
----------------

To return a new value, simply call the Choice object. 


    >>> where_to_go = Choice({"Paris": 0.4, "London": 0.4, "Copenhagen": 0.1, "Barcelona": 0.1 })
    >>> where_to_go()
    'Copenhagen'


Finding probabilities
---------------------

You can retrieve the distribution of how those values are applied
by accessing the distribution attribute:

    >>> mood.distribution
    [('happy', 0.3), ('neutral', 0.6), ('sad', 0.1)]
    
    >>> where_to_go.distribution
    [('Paris': 0.4), ('London', 0.4), ('Copenhagen', 0.1), ('Barcelona', 0.1)]

Retrieving the probability of a particular key is supported. However,
the search strategy is very inefficient and probably shouldn't be used
outside of the interactive Python shell.

    >>> birds['geese']
    0.0
"""

import random

class Choice(object):
    """
    >>> mood = Choice([('happy', 0.3), ('neutral', 0.6), ('sad', 0.1)])
    >>> mood()
    'happy'
    >>> mood()
    'neutral'
    """
    def __init__(self, dist, ranfun=random.random):
        if hasattr(dist, 'iteritems'):
            dist = [(k,p) for k,p in dist.iteritems()]
        self.nominal_distribution = dist
        self.distribution = self.__normalise_dist(dist)
        self._cumulative_distribution = self.__gen_cumul_dist()
        self._ranfun = ranfun
    
    def __contains__(self, item):
        return item in [key for key, p in self.distribution]

    def __normalise_dist(self, dist):
        s = sum(p for key,p in dist)
        s = float(s)
        q = [p/s for key,p in dist]
        keys = [key for key,p in dist]
        dist = zip(keys, q)
        dist = sorted(dist, key=lambda el: el[1])
        return dist

    def __gen_cumul_dist(self):
        dist = self.distribution[:]
        dist.reverse()
        so_far = 0
        for i, (key, p) in enumerate(dist):
            dist[i] = (key, p + so_far)
            so_far = so_far + p
        return dist

    def __getitem__(self, key):
        for item, p in self.distribution:
            if key == item:
                return p
        raise KeyError

    def __repr__(self):
        return u'Choice({0})'.format(self.nominal_distribution)

    def __call__(self):
        choice = self._ranfun()
        for key, val in self._cumulative_distribution:
            if choice <= val:
                return key

