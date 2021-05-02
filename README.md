[![Build Status](https://travis-ci.org/anirudh-acharya/monopoly.png?branch=master)](https://travis-ci.org/anirudh-acharya/monopoly)
[![Code Coverage Status](http://codecov.io/github/anirudh-acharya/monopoly/coverage.svg?branch=master)](http://codecov.io/github/anirudh-acharya/monopoly?branch=master)
[![Requirements Status](https://requires.io/github/anirudh-acharya/monopoly/requirements.svg?branch=master)](https://requires.io/github/anirudh-acharya/monopoly/requirements/?branch=master)

# monopoly
A webapp to keep track of a monopoly game transactions

# Installation steps
1. Setup virtualenv
```
$ virtualenv django
```
2. Activate virtualenv
```
$ source django/bin/activate
```
3. Install requirements
```
$ pip install -r requirements.txt
```
4. Apply migrations
```
$ python manage.py migrate
```
5. Run server
```
$ python manage.py runserver
```

# How to test
```
$ python manage.py test
```

# Test data setup
1. 3 Users, alice, bob, carol, and another user bank
2. 1 test game created with alice, and bob as the players


