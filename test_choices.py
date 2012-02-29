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

from collections import Counter

from choices import PDist

def test_list_of_tuple_form():
    assert PDist([('a', 0.9), ('b', 0.1)])

def test_dict_form():
    assert PDist({'cat': 0.98, 'mouse': 0.02})

def test_sample_form():
    a =  PDist([('a', 0.9), ('b', 0.1)])
    b =  PDist([('a', 9), ('b', 1)])
    assert a.distribution == b.distribution

def test_cumulative_dist_is_sorted():
    a =  PDist([('a', 0.9), ('b', 0.1)])
    print a._cumulative_distribution
    print a._cumulative_distribution[0]
    assert a._cumulative_distribution[0] == ('a', 0.9)
    assert a._cumulative_distribution[1] == ('b', 1.0)

def test_that_a_uniform_dist_ends_up_roughly_uniform():
    a = PDist([(x, 1) for x in 'abcd'])
    results = Counter(a() for _ in range(10000))
    print results
    for letter in 'abcd':
        assert 2400 < results[letter] < 2600

def test_that_an_uneven_distribution_stays_uneven():
   a = PDist({'lots':0.7, 'few':0.3})
   results = Counter(a() for _ in range(10000))
   print results
   assert 6800 < results['lots'] < 7200
   assert results['lots'] + results['few'] == 10000
