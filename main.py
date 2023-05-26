import nltk
from nltk.tree import Tree
from itertools import permutations
import re

import lexicon

formalizations = lexicon.event_lexicon
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
def get_verb_position(tree):
    for node in tree.treepositions(order="leaves"):
        if tree[get_parent_node(node)].label() in ["Vi", "Vt"]:
            return node


# Define a function that takes a parse tree, and returns the position of the subject DP.
def get_subject_position(tree):
    VP_pos = (-1,)
    for node in tree.treepositions(order="preorder"):
        if isinstance(tree[node], nltk.Tree):  # Check if node has children
            if tree[node].label() == "VP":
                VP_pos = node
            if node[:len(VP_pos)] != VP_pos and tree[node].label() == "DP":
                return node


# Define a function that takes a parse tree, and returns the position of the object DP
# if one exists, and None otherwise
def get_object_position(tree):
    VP_pos = (-1,)
    for node in tree.treepositions(order="preorder"):
        if isinstance(tree[node], nltk.Tree):  # Check if node has children
            if tree[node].label() == "VP":
                VP_pos = node
            if node[:len(VP_pos)] == VP_pos and tree[node].label() == "DP":
                return node


# Define a function that returns a list of positions in the tree, corresponding to all quantifier DPs
# (i.e., the constituents that might undergo quantifier raising, which will be implemented later).
def get_quantifier_DP_positions(tree):
    DPs = []
    for node in tree.treepositions():
        if isinstance(tree[node], nltk.Tree):  # Check if node has children
            if tree[node].label() == "Det":
                DPs.append(get_parent_node(node))
    return DPs


def print_tree_data(tree):
    tree.pretty_print()
    print('verb position: ', get_verb_position(tree))
    print('subject position: ', get_subject_position(tree))
    print('object position: ', get_object_position(tree))
    print('quantifier DPs: ', get_quantifier_DP_positions(tree))


for t in trees:
    print_tree_data(t)

existentials = ['a', 'some', 'an']
universal = ['every']


def check_quantified_children(tree, node):
    quantified = get_quantifier_DP_positions(tree)
    return (tree[node + (1,)] in quantified) or (tree[node + (0,)] in quantified)


def formalize_single_node(node, translations):
    if isinstance(node, nltk.Tree):
        if not node[:-1]:  # that is, if there is only one child node
            return formalize_single_node(node[0], translations)
        right_node = formalize_single_node(node[1], translations)
        if right_node.type == 't':
            trace_name = node[0].label().replace('DP', 't')
            return right_node.remove_traces(trace_name).application(formalize_single_node(node[0], translations))
        else:
            return formalize_single_node(node[0], translations).application(formalize_single_node(node[1], translations))
    elif re.match(r"t\d+", node):  # if it is a trace
        return lexicon.formalizations['PropN'](node)
    else:
        return translations[node]


def translate_to_logic(tree=nltk.Tree, use_events=False):
    if use_events:
        translation_method = lexicon.event_lexicon
    else:
        translation_method = lexicon.extensional_lexicon
    top_node_formalization = formalize_single_node(tree[()], translation_method)
    if type(top_node_formalization.formula) == str:
        return top_node_formalization.formula
    else:
        return top_node_formalization.string


def create_event_tree(base_tree):
    tree = base_tree.copy()
    subj_pos = get_subject_position(tree)
    tree[subj_pos] = Tree('ThetaP', [Tree('Role', ['agent']), tree[subj_pos]])
    if obj_pos := get_object_position(tree):
        tree[obj_pos] = Tree('ThetaP', [Tree('Role', ['patient']), tree[obj_pos]])
    tree = Tree('EP', [Tree('Event', ['ev_exists']), tree])
    return tree


def fix_root_system(tree):  # Function to only make one node the S node and the sub nodes the S_sub
    for node in tree.treepositions('postorder'):
        if len(node) > 0 and isinstance(tree[node], nltk.Tree) and tree[node].label() == 'S':
            tree[node] = nltk.Tree('SUB_S', [n for n in tree[node]])
    return tree


def raise_node(tree=nltk.Tree, n_pos=tuple, replacement_='', new_label=''):  # Raise a node to the top of the tree
    tree = tree.copy(deep=True)
    dp_pos = nltk.Tree(new_label, [n for n in tree[n_pos]])
    tree[n_pos] = replacement_
    return nltk.Tree('S', [dp_pos, tree])


def quantifier_possibilities(tree=nltk.Tree, by='DP'):  # Calculate all possible trees for translate_to_logic()
    quantifiers = [node for node in tree.treepositions(order='postorder') if isinstance(tree[node], nltk.Tree) and sum([1 if x in existentials + universal else 0 for x in tree[node].leaves()]) > 0 and tree[node].label() == by]
    possibilities = []
    for possibility in permutations(quantifiers, len(quantifiers)):
        new_tree = tree.copy(deep=True)
        for index, node in enumerate(possibility):
            for i in range(index):
                node = (1,) + node
            new_tree = raise_node(new_tree, node, replacement_=f't{index+1}', new_label=f'{by}{index+1}')
        new_tree = fix_root_system(new_tree)
        possibilities.append(new_tree)
    return possibilities


def show_all_formulas(tree):
    tree = create_event_tree(tree)
    for possibility in quantifier_possibilities(tree):
        possibility.pretty_print()
        # print(translate_to_logic(possibility)[()].formula)
        print(translate_to_logic(possibility, use_events=True))


for t in trees:
    # print(translate_to_logic2(t))
    show_all_formulas(t)
