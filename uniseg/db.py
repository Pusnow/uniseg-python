from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import errno
import os
import sqlite3
import sys

from .codepoint import ord


def print_dbpath():

    """Print the path of the database file. """

    print(os.path.abspath(_dbpath))


def find_dbpath():

    """Find the database file in the specified order and return its path.

    The search paths (in the order of priority) are:
    1. The directory of the package,
    2. that of the executable
    3. and the current directory.
    """
    dbname = 'ucd.sqlite3'
    
    dbpath = os.path.join(os.path.dirname(__file__), dbname)
    if (os.path.exists(dbpath)):
        return dbpath

    dbpath = os.path.join(os.path.dirname(sys.executable), dbname)
    if (os.path.exists(dbpath)):
        return dbpath

    dbpath = os.path.join(os.getcwd(), dbname)
    if (os.path.exists(dbpath)):
        return dbpath

    return None


_dbpath = find_dbpath()
if _dbpath:
    _conn = sqlite3.connect(_dbpath)
else:
    _conn = None

db = dict()
cur = _conn.cursor()

cur.execute('select cp, value from GraphemeClusterBreak')
db["GraphemeClusterBreak"] = dict()
for cp, value, in cur:
    db["GraphemeClusterBreak"][cp] = value

cur.execute('select cp, value from WordBreak')
db["WordBreak"] = dict()
for cp, value, in cur:
    db["WordBreak"][cp] = value

cur.execute('select cp, value from SentenceBreak')
db["SentenceBreak"] = dict()
for cp, value, in cur:
    db["SentenceBreak"][cp] = value

cur.execute('select cp, value from LineBreak')
db["LineBreak"] = dict()
for cp, value, in cur:
    db["LineBreak"][cp] = value

def grapheme_cluster_break(u):

    u = ord(u)
    if u in db["GraphemeClusterBreak"]:
        return str(db["GraphemeClusterBreak"][u])
    return 'Other'


def iter_grapheme_cluster_break_tests():
    
    cur = _conn.cursor()
    cur.execute('select name, pattern, comment from GraphemeClusterBreakTest')
    return iter(cur)


def word_break(u):
    
    u = ord(u)
    if u in db["WordBreak"]:
        return str(db["WordBreak"][u])
    return 'Other'


def iter_word_break_tests():
    
    cur = _conn.cursor()
    cur.execute('select name, pattern, comment from WordBreakTest')
    return iter(cur)


def sentence_break(u):
    
    u = ord(u)
    if u in db["SentenceBreak"]:
        return str(db["SentenceBreak"][u])
    return 'Other'


def iter_sentence_break_tests():
    
    cur = _conn.cursor()
    cur.execute('select name, pattern, comment from SentenceBreakTest')
    return iter(cur)


def line_break(u):
    
    u = ord(u)
    if u in db["LineBreak"]:
        return str(db["LineBreak"][u])
    return 'Other'


def iter_line_break_tests():
    
    cur = _conn.cursor()
    cur.execute('select name, pattern, comment from LineBreakTest')
    return iter(cur)
