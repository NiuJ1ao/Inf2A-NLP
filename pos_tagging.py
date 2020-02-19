# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    NNwords = []
    words = []
    with open("sentences.txt", "r") as f:
        for line in f:
            # add code here
            m = re.findall(r"(\w+)\|(\w+)", line)
            for word, tag in m:
                if tag == "NN" and word not in NNwords:
                    NNwords.append(word)
            
            for word, tag in m:
                if tag == "NNS" and word in NNwords and word not in words:
                    words.append(word)

    return words        

unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    # add code here
    if s in unchanging_plurals_list:
        return s

    if re.match(r"\w*men", s):
        return s[:-2] + "an"

    # NNS = False
    # for word, tag in brown.tagged_words():
    #     if word == s and tag[:3] == "NNS":
    #         NNS = True
    #         break
    
    # if not NNS:
    #     return ""

    if (re.match(r"\w+[^sxyzaeiou(ch)(sh)]s", s)):
        return s[:-1]

    if (re.match(r"\w+[aeiou]ys", s)):
        return s[:-1]
    
    if (re.match(r"\w+[^aeiou]ies", s)):
        return s[:-3] + "y"
    
    if (re.match(r"[^aeiou]ies", s)):
        return s[:-1]
    
    if (re.match(r"(\w+)[ox]es|(\w+)(ch|sh|ss|zz)es" , s)):
        return s[:-2]

    if (re.match(r"[^(sse)(zee)]", s[-4:-2])):
        if (re.match(r"\w+((se)|(ze))s", s)):
            return s[:-1]

    if (re.match(r"\w+[^iosxz]es|\w+(^ch|^sh)es", s)):
        return s[:-1]

    return ""


def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    # add code here
    tags = []
    lxtags = ['P','N','A','I','T']
    for word, tag in function_words_tags:
        if word == wd:
            tags.append(tag)
            return tags
    
    # if wd is noun or verb
    if verb_stem(wd) != "":
        # it is VBZ
        # tags.append("Ts")
        for tag in ['P','N','A','I', 'T']:
            for word in lx.getAll(tag):
                if verb_stem(wd) == word:
                    if tag == 'I' or tag == 'T':
                        tags.append(tag+'s')
                    elif tag == 'N':
                        tags.append(tag+'p')
                    break
        # print(tags)
        return tags
    
    if noun_stem(wd) != "":
        # it is NNS
        if noun_stem(wd) == wd:
            tags.append("Ns")
            tags.append("Np")
            for tag in ['P','A','I','T']:
                for word in lx.getAll(tag):
                    if wd == word:
                        if tag == 'I' or tag == 'T':
                            tags.append(tag + 'p')
                        else:
                            tags.append(tag)
                        break
        else:
            tags.append("Np")       
            for tag in ['P','A','I','T']:
                for word in lx.getAll(tag):
                    if noun_stem(wd) == word:
                        if tag == 'I' or tag == 'T':
                            tags.append(tag+'s')
                        else:
                            tags.append(tag)
                        break
        # print(tags)
        return tags
           
    
    for tag in lxtags:
        words = lx.getAll(tag)
        for word in words:
            if wd == word: 
                if tag == 'N':
                    tags.append(tag + 's')
                elif tag == 'I' or tag == 'T':
                    tags.append(tag + 'p')
                else:
                    tags.append(tag)

                break
    # print(tags)           
    return tags
            


def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.
  
if __name__ == "__main__":
    lx = Lexicon()
    lx.add("John", 'P')
    lx.add("Mary", 'P')
    lx.add("duck", 'N')
    lx.add("student", 'N')
    lx.add('orange', 'N')
    lx.add('fish', 'N')
    lx.add("purple", 'A')
    lx.add('old', 'A')
    lx.add('orange', 'A')
    lx.add('fly', 'I')
    lx.add('swim', 'I')
    lx.add('fish','I')
    lx.add('like', 'I')
    lx.add('like', 'T')
    lx.add("fish", 'T')
    lx.add('hit', 'T')
    print(tag_word(lx, "flies"))