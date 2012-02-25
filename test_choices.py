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


def test_list_of_tuple_form():
    assert PDist([('a', 0.9), ('b', 0.1)])

def test_dict_form():
    assert PDist({'cat': 0.98, 'mouse': 0.02})

def test_sample_form():
    a =  PDist([('a', 0.9), ('b', 0.1)])
    b =  PDist([('a', 9), ('b', 1)])
    assert a.distribution == b.distribution

