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

# # select the verb for the sentence 'john sees mary'
# print(trees[0][1, 0])
# # select the subject for the sentence 'john sees mary'
# print(trees[0][0])
# # select the determiner for sentence 'A student walks'
# print(trees[1][0, 0])
# print('\n')
#
# # practice iterating
# for sub in trees[2].subtrees():
#     print(sub)
# print('\n')
# for pos in trees[2].treepositions():
#     print(pos)
# print('\n')
# for pos in trees[2].treepositions(order="leaves"):
#     print(pos)
# print('\n')
# for pos in trees[2].treepositions(order="postorder"):
#     print(pos)
# print('\n')


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


def quantifier_raising(tree, nb, position):
    tree_ = tree.copy(deep=True)
    for i in range(nb - 1):
        new_position = (1,) + position
        position = new_position
        # print(f'the position is {position}')

    qp = tree_[position]
    tree_[position] = Tree('Trace', [f't{nb}'])
    print('after trace added \n')
    tree_.pretty_print()

    tree_ = nltk.Tree(f'S{nb}', [qp, tree_])
    tree_[0].set_label(f'DP{nb}')
    return tree_


def raiser(tree=nltk.Tree):
    tree_list = []
    tree1 = tree.copy(deep=True)
    quant_dict = {}
    for node in tree1.treepositions(order='postorder'):
        if (tree1[node] in existentials) or (tree1[node] in universal):
            quant_dict[node[:-2]] = tree1[node[:-2]]
    print(quant_dict)
    nb = 0
    print('First Version \n')
    for key in quant_dict.keys():
        # print(quant_dict[key])

        nb += 1
        tree1 = quantifier_raising(tree1, nb, key)
        tree1.pretty_print()
    tree_list.append(tree1)
    if len(quant_dict) == 2:  # if there is another QP we will generate a new possible structure
        tree2 = tree.copy(deep=True)
        nb = 0
        print('Second Version \n')
        for key in reversed(quant_dict.keys()):
            print(quant_dict[key])
            nb += 1
            tree2 = quantifier_raising(tree2, nb, key)
            tree2.pretty_print()
    tree_list.append(tree2)
    return tree_list


def quantifier_logic(tree=nltk.Tree):
    traces = {}
    tree = tree.copy(deep=True)
    for node in tree.treepositions(order="postorder"):
        if isinstance(tree[node], nltk.Tree):
            if len(tree[node]) > 1:
                if tree[node].label() == 'S':
                    basic_tree = tree[node]
                    base_logic = translate_to_logic(
                        basic_tree)  # get the logicial form from below the raised quantifiers
            if tree[node].label() == 'Trace_e':
                traces[tree[node, 0]] = node + (0,)  # collect traces positions and names in a dictionary
    # print(traces)
    subtree_logic = {}
    for trace in traces.keys():  # now we will slowly do lambda abstraction per raised quantifier
        trace_number = trace[-1]
        for node in tree.treepositions(order="postorder"):
            if isinstance(tree[node], nltk.Tree):
                if len(tree[node]) > 1:
                    if tree[node].label() == f'DP{trace_number}':
                        subtree = tree[node].copy(deep=True)
                        subtree.set_label('DP')
                        sub_tree = nltk.Tree('S', [subtree,
                                                   Tree('VP', [Tree('Vi', ['t_verb'])])])  # added a dummy verb because
                        # the logic function does not like computing things without a verb
                        # sub_tree.pretty_print()
                        sub_logic = translate_to_logic(sub_tree)
                        # print(sub_logic[()].formula)
                        subtree_logic[trace] = sub_logic[()].formula

    variables = ['x', 'y', 'z']
    t = 0
    # trace_iteration = subtrees[list(subtrees.keys())[0]]
    new_logic = base_logic[()].formula

    for trace in subtree_logic.keys():
        subtree_logic[trace] = re.sub(r'(\W)x(\W)', '\\1' + variables[t] + '\\2', subtree_logic[trace])
        trace_logic = subtree_logic[trace]
        new_logic = re.sub(r'T_VERB\(' + variables[t] + r'\)', new_logic, trace_logic)  # fill predicate
        # print(new_logic)
        new_logic = re.sub(trace, variables[t], new_logic)  # fill trace with variable
        t += 1

        logic = new_logic
    return logic


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


def translate_to_logic2(tree=nltk.Tree, use_events=False):
    if use_events:
        translation_method = lexicon.event_lexicon
    else:
        translation_method = lexicon.extensional_lexicon
    top_node_formalization = formalize_single_node(tree[()], translation_method)
    if type(top_node_formalization.formula) == str:
        return top_node_formalization.formula
    else:
        return top_node_formalization.string


def translate_to_logic(tree=nltk.Tree):
    result = {}
    prev_was_leaf = False
    leaf = ''
    root_cause = None
    for node in tree.treepositions(order='postorder'):
        if not isinstance(tree[node], nltk.Tree):
            prev_was_leaf = True
            leaf = tree[node]
            if re.match(r"t\d+", leaf):
                result[node] = lexicon.formalizations['PropN'](leaf)
        elif len(tree[node]) > 1:
            if tree[node].label() == 'S':
                result[node] = result[node + (0,)].application(result[node + (1,)])
            else:
                if not isinstance(tree[node + (0,)], nltk.Tree):  # If a t is in zero position apply flipped
                    if re.match(r't\d+', tree[node + (0,)]):
                        result[node] = result[node + (1,)].application(result[node + (0,)])
                else:
                    result[node] = result[node + (0,)].application(result[node + (1,)])
                if tree[node].label() == 'VP' and check_quantified_children(tree, node):
                    return None
        elif prev_was_leaf:
            result[node] = formalizations[leaf]
            root_cause = result[node]
            prev_was_leaf = False
        elif not re.match(r"t\d+", leaf):
            result[node] = root_cause

    return result


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
        print(translate_to_logic2(possibility, use_events=True))


for t in trees:
    # print(translate_to_logic2(t))
    show_all_formulas(t)
