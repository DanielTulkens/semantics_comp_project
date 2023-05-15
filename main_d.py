import nltk
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

parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)

sentences = ['John sees Mary', 'A student walks', 'Some girl sees every boy', 'Every eager student passed']


def create_parse_tree(sentence):
    tokens = sentence.lower().split()
    parse_trees = parser.parse(tokens)
    if not parse_trees:
        return
    for parse_tree in parse_trees:
        return parse_tree


def select_verb(parse_tree):
    for position in parse_tree.treepositions():
        if parse_tree[position].label() == "V":
            if parse_tree[position + (0,)].label() == "Vbar":
                position += (0,)
            else:
                break


def print_sentence_data(sentence):
    parse_tree = create_parse_tree(sentence)
    if not parse_tree:
        print("No parse tree found.")
        return
    parse_tree.pretty_print()
    print(parse_tree.treepositions())


for s in sentences:
    print_sentence_data(s)
