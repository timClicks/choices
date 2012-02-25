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
The PDist is designed to make it easy to make it easy to make 
things happen in a probablistic manner. Provide keys with an 
associated probability attached, and the

    >>> mood = PDist({'happy': 0.3, 'neutral': 0.6, 'sad': 0.1})
    >>> mood()
    'happy'
    >>> mood()
    'neutral'

You can retrieve the distribution of how those values are applied
by accessing the distribution attribute:

    >>> mood.distribution
    [('happy', 0.3), ('neutral', 0.6), ('sad', 0.1)]

As well as a dict assigning a probability to each key, you can
send in a list of lists/tuples. This allows for for non-hashable
types to be used. This means that you provide objects such as 
functions to be used as keys:

  >>> def grumpy(news):
  ...    return ':/'
  >>> def happy(news):
  ...    return ':)'
  >>> react = PDist([(grumpy, 0.7), (happy, 0.3)])
  >>> reaction = react()
  >>> reaction("We're getting married!")
  ':/'

You are not restricted to adding p to 1. If you only have samples,
and wish to calculate a probablilty distribution, you can provide 
those too:

   >>> spotted = {'geese': 0, 'ducks': 12, 'sparrows': 4, 'other': 39}
   >>> bird_pdist = PDist(spotted)
   >>> bird_pdist.distribution
   [('geese', 0.0), ('sparrows', 0.07272727272727272), ('ducks', 0.21818181818181817), ('other', 0.7090909090909091)]

Retrieving the probability of a particular key is supported. However,
the search strategy is very inefficient and probably shouldn't be used
outside of the interactive Python shell.

    >>> bird_pdist['geese']
    0.0
"""

import random

class PDist(object):
    """
    >>> mood = PDist([('happy', 0.3), ('neutral', 0.6), ('sad', 0.1)])
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
        return u'PDist({0})'.format(self.nominal_distribution)

    def __call__(self):
        choice = self._ranfun()
        for key, val in self._cumulative_distribution:
            choice = choice - val
            if choice <= 0:
                return key

