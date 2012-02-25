import choices

from distutils.core import setup
setup(
  name='choices',
  version='0.1',
  py_modules=['choices'],
  description="Making choices from a probability distribution",
  author="Tim McNamara",
  author_email="paperless@timmcnamara.co.nz",
  long_description = choices.__doc__,
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ]
)

