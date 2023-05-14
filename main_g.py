import nltk
from nltk.tree import Tree
import sys 
import random

grammar = nltk.CFG.fromstring("""
    S -> NP VP
    NP -> Det N | N | PropN | Adj NP | NP PP
    VP -> V | Vbar NP | Vbar NP PP | Adv VP | VP Adv | VP Conj VP | V AdvP
    Vbar -> V
    AdvP -> Adv P
    PP -> P NP
    Det -> 'a' | 'an' | 'the' | 'every'| 'some' | 'any'
    P -> 'with' | 'in' | 'on' | 'to' | 'without' | 'from'
    Conj -> 'and' | 'or' | 'but'


    N -> 'boy' | 'student' | 'girl' | 'class' | 'book' | 'teacher'
    PropN -> 'john' | 'mary'
    Adj -> 'eager' | 'smart'
    V -> 'walks' | 'passed' | 'sees' | 'studies' | 'teaches' | 'saw' 
    Adv -> 'eagerly' | 'well'
    
""")

sentences = [ 'John sees Mary', 'A student walks', 'Some girl sees every boy','Every eager student passed']


# sentence = random.choice(sentences)
sentence = sentences[0]
parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                  
tokens = sentence.lower().split()
parse_trees = parser.parse(tokens)
if not parse_trees:
    print("No parse tree found.")
for parse_tree in parse_trees:
    print(parse_tree)

#pretty_print

parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                
tokens = sentence.lower().split()
parse_trees = parser.parse(tokens)
if not parse_trees:
    print("No parse tree found.")
for parse_tree in parse_trees:
    parse_tree.pretty_print()

#select the verb for the sentence 'john sees mary' 
print(parse_tree[1,0])
#select the subject for the sentence 'john sees mary'
print(parse_tree[0])
#select the determiner for sentence 'A student walks'
sentence = sentences[1]
tokens = sentence.lower().split()
parse_trees = parser.parse(tokens)
for parse_tree in parse_trees:
    parse_tree.pretty_print()
print(parse_tree[0,0])

#practice iterating
# for subtree in parse_tree.subtrees(): 
#     print(subtree)
# for pos in parse_tree.treepositions(): ...
# for pos in treepositions(order="leaves"): ...
# for pos in treepositions(order="postorder")


