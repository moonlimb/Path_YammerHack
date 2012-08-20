from distutils.core import setup

long_description = open('README.rst').read()

setup(name="python-yammer",
      version='0.2.1',
      py_modules=["yammer"],
      description="Library for interacting with the Yammer API",
      author="James Turk, Adam Gschwender",
      author_email = "jturk@sunlightfoundation.com, adam.gschwender@mccann.com",
      license="BSD",
      url="http://github.com/McCannErickson/python-yammer/",
      long_description=long_description,
      platforms=["any"],
      install_requires=["oauth2"],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
      )
