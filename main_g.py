import nltk
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


sentence = random.choice(sentences)
parser = nltk.parse.RecursiveDescentParser(grammar)                            
tokens = sentence.lower().split()
parse_trees = parser.parse(tokens)
if not parse_trees:
    print("No parse tree found.")
for parse_tree in parse_trees:
    print(parse_tree)

#pretty_print
sentence = random.choice(sentences)
parser = nltk.parse.RecursiveDescentParser(grammar)                            
tokens = sentence.lower().split()
parse_trees = parser.parse(tokens)
if not parse_trees:
    print("No parse tree found.")
for parse_tree in parse_trees:
    parse_tree.pretty_print()

#select the verb 



