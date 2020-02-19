# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    # add code here
    def __init__(self):
        self.p = []
        self.n = []
        self.a = []
        self.i = []
        self.t = []

    def add(self, stem, cat):
        if cat == 'P':
            self.p.append(stem)
        elif cat == 'N':
            self.n.append(stem)
        elif cat == 'A':
            self.a.append(stem)
        elif cat == 'I':
            self.i.append(stem)
        elif cat == 'T':
            self.t.append(stem)

    def getAll(self, cat):
        if cat == 'P':
            return list(set(self.p))
        elif cat == 'N':
            return list(set(self.n))
        elif cat == 'A':
            return list(set(self.a))
        elif cat == 'I':
            return list(set(self.i))
        elif cat == 'T':
            return list(set(self.t))
        

class FactBase:
    """stores unary and binary relational facts"""
    # add code here
    def __init__(self):
        self.unary = list()
        self.binary = list()

    def addUnary(self, pred, e1):
        self.unary.append((pred, e1))

    def addBinary(self, pred, e1, e2):
        self.binary.append((pred, e1, e2))

    def queryUnary(self, pred, e1):
        result = False
        for k,v in self.unary:
            if pred == k and e1 == v:
                result = True
                break

        return result

    def queryBinary(self, pred, e1, e2):
        result = False
        for k, v1, v2 in self.binary:
            if pred == k and e1 == v1 and e2 == v2:
                result = True
                break

        return result

import re
from nltk.corpus import brown 
def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    # add code heres
    # vowel = ["a", "e", "i", "o", "u"]
    if s == "are" or s == "have" or s == "do":
        return ""

    VBZ = False
    for word, tag in brown.tagged_words():
        # if word == s:
        #     print(word + tag)
        if word == s and tag[:3] == "VBZ":
            # print(tag[:3])
            VBZ = True
            break
    
    if not VBZ:
        # print("1")
        return ""

    if (re.match(r"\w+[^sxyzaeiou]s", s)):
        return s[:-1]

    if (re.match(r"\w+[aeiou]ys", s)): # If the stem ends in y preceded by a vowel, simply add s (pays, buys)
        return s[:-1]
    
    if (re.match(r"\w+[^aeiou]ies", s)):
        return s[:-3] + 'y'
    
    if (re.match(r"[^aeiou]ies", s)):
        return s[:-1]
    
    if (re.match(r"(\w+)[ox]es|(\w+)(ch|sh|ss|zz)es" , s)):
        return s[:-2]

    if (re.match(r"[^(sse)(zee)]", s[-4:-2])):
        if (re.match(r"\w+((se)|(ze))s", s)):
            return s[:-1]
        
    if (re.match(r"has", s)):
        return "have"

    if (re.match(r"\w+[^iosxz]es|\w+(^ch|^sh)es", s)):
        return s[:-1]

    return ""

    
def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.

