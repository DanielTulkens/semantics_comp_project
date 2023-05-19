import nltk
from nltk.tree import Tree
import sys 
import random

import lexicon

formalizations = lexicon.extensional_lexicon
grammar = nltk.CFG.fromstring(lexicon.extensional_grammar)

parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)

sentences = ['John sees Mary',
             'A student walks',
             'Some girl sees every boy',
             'Every eager student passed'
             ]


def create_parse_tree(sentence):
    tokens = sentence.lower().split()
    parse_trees = parser.parse(tokens)
    if not parse_trees:
        return
    for parse_tree in parse_trees:
        return parse_tree


trees = [create_parse_tree(sentence) for sentence in sentences]

# select the verb for the sentence 'john sees mary'
print(trees[0][1, 0])
# select the subject for the sentence 'john sees mary'
print(trees[0][0])
# select the determiner for sentence 'A student walks'
print(trees[1][0, 0])
print('\n')

# practice iterating
for subtree in trees[2].subtrees():
    print(subtree)
print('\n')
for pos in trees[2].treepositions():
    print(pos)
print('\n')
for pos in trees[2].treepositions(order="leaves"):
    print(pos)
print('\n')
for pos in trees[2].treepositions(order="postorder"):
    print(pos)
print('\n')


# Define a function that takes a position in the parse tree (i.e., a tuple like (0, 1, 1))
# and returns the position of the parent node ((0, 1) in this case), or None if it has no parent.
def get_parent_node(child_tuple):
    if len(child_tuple) >= 1:
        parent_node = child_tuple[:-1]
        return parent_node
    else:
        return None


# Define a function that takes a parse tree, and returns the position of the verb (i.e., a tuple).
# If your grammar follows the textbook closely, then the position of the verb will depend on
# whether it is a transitive or intransitive verb (i.e., depending on the presence/absence of a Vbar node).
def get_verb_pos(tree):
    for node in tree.treepositions(order="leaves"):
        if tree[get_parent_node(node)].label() in ["Vi", "Vt"]:
            return node


# Define a function that takes a parse tree, and returns the position of the subject DP.
def get_subject_pos(tree):
    VP_pos = (-1,)
    for node in tree.treepositions(order="preorder"):
        if isinstance(tree[node], nltk.Tree):  # Check if node has children
            if tree[node].label() == "VP":
                VP_pos = node
            if node[:len(VP_pos)] != VP_pos and tree[node].label() == "DP":
                return node


# Define a function that takes a parse tree, and returns the position of the object DP
# if one exists, and None otherwise
def get_object_pos(tree):
    VP_pos = (-1,)
    for node in tree.treepositions(order="preorder"):
        if isinstance(tree[node], nltk.Tree):  # Check if node has children
            if tree[node].label() == "VP":
                VP_pos = node
            if node[:len(VP_pos)] == VP_pos and tree[node].label() == "DP":
                return node


# Define a function that returns a list of positions in the tree, corresponding to all quantificational DPs
# (i.e., the constituents that might undergo quantifier raising, which will be implemented later).
def get_quantificational_DPs(tree):
    pass


def print_tree_data(tree):
    tree.pretty_print()
    print('verb position: ', get_verb_pos(tree))
    print('subject position: ', get_subject_pos(tree))
    print('object position: ', get_object_pos(tree))
    print('quantificational DPs: ', get_quantificational_DPs(tree))


for t in trees:
    print_tree_data(t)

# assignment 6
existentials = ['a', 'some', 'an']
universal = ['every']


def translate_to_logic(tree=nltk.Tree):
    result = {}
    prev_was_leave = False
    leaf = ''
    root_cause = None
    for node in tree.treepositions(order='postorder'):
        if isinstance(tree[node], nltk.Tree):
            if len(tree[node]) > 1:
                if tree[node].label() == 'S':
                    if result[node + (1,)].t == 'existential':
                        result[node] = result[node + (0,)].application(result[node + (1,)])
                    else:
                        result[node] = result[node + (1,)].application(result[node + (0,)])
                else:
                    result[node] = result[node + (0,)].application(result[node + (1,)])
            else:
                if prev_was_leave:
                    if leaf in existentials:
                        applier = 'existential'
                    elif leaf in universal:
                        applier = 'universal'
                    else:
                        applier = tree[node].label()
                    result[node] = formalizations[applier][leaf]
                    root_cause = result[node]
                    prev_was_leave = False
                else:
                    result[node] = root_cause
        else:
            prev_was_leave = True
            leaf = tree[node]
    return result


res = translate_to_logic(create_parse_tree(sentences[0]))
res[()].formula
