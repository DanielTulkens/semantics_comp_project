# %%
import nltk
from nltk.tree import Tree
import re
import sys 
import random 

# %%
grammar = nltk.CFG.fromstring("""
    S -> DP VP
    DP -> Det NP | NP | DP Conj DP | Trace_e | Trace_T
    NP -> N | PropN | Adj NP | NP PP
    VP -> Vi | Vt  | Vpro | Vbar DP | Vbar CP | Vbar DP PP | Adv VP | VP Adv | VP Conj VP | V AdvP
    Vbar -> Vi | Vt | Vpro
    CP -> C Cbar
    Cbar -> DP VP
    AdvP -> Adv P
    PP -> P DP
    
    Det -> 'a' | 'an' | 'the' | 'every'| 'some' | 'any'
    P -> 'with' | 'in' | 'on' | 'to' | 'without' | 'from'
    Conj -> 'and' | 'or' | 'but'
    C -> 'that'


    N -> 'boy' | 'student' | 'girl' | 'class' | 'book' | 'teacher'
    PropN -> 'john' | 'mary'
    Adj -> 'eager' | 'smart'
    Vi -> 'walks' | 'passed' 
    Vt -> 'sees' | 'teaches'
    Vpro -> 'thinks' | 'believes'
    Adv -> 'eagerly' | 'well'
    Trace_e -> 't1' | 't2' | 't3'
    Trace_t -> 't1' | 't2' | 't3'
    
""")

# %%
sentences = [ 'John sees Mary', 'A student walks', 'Some girl sees every boy','Every eager student passed']

# %%
# sentence = random.choice(sentences)
sentence = sentences[2]
parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                  
tokens = sentence.lower().split()
parse_trees = parser.parse(tokens)
if not parse_trees:
    print("No parse tree found.")
for parse_tree in parse_trees:
    print(parse_tree)

# %% [markdown]
# assignment 2

# %%
parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                
tokens = sentence.lower().split()
parse_trees = parser.parse(tokens)
if not parse_trees:
    print("No parse tree found.")
for parse_tree in parse_trees:
    parse_tree.pretty_print()

# %%
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
print('\n' )

#practice iterating
for subtree in parse_tree.subtrees(): 
    print(subtree)
print('\n' )
for pos in parse_tree.treepositions(): 
    print(pos)
print('\n')
for pos in parse_tree.treepositions(order="leaves"):
    print(pos)
print('\n')
for pos in parse_tree.treepositions(order="postorder"):
  print(pos)
print('\n')

#get parent node 

def get_parent_node(child_tuple): 
    if len(child_tuple) >= 1: 
        parent_node = child_tuple[:-1]
        return parent_node
    else: 
        return None

#get verb tuple 
def get_verb_tuple(tree):
    for node in tree.treepositions(order="leaves"):
        if tree[get_parent_node(node)].label() in ["Vi", "Vt"]:
            return node

verb = get_verb_tuple(parse_tree) #calling the get verb 
print(parse_tree.pretty_print())
print(verb)



# #Define a function that takes a parse tree, and returns the position of the subject DP.
def get_subj_pos(tree):
    VP_pos = (-1,)
    for node in tree.treepositions(order="preorder"):
        if isinstance(tree[node], nltk.Tree): #Check if node has children
            if tree[node].label() == "VP":
                VP_pos = node
            if node[:len(VP_pos)] != VP_pos and tree[node].label() == "DP":
                return node

dp = get_subj_pos(parse_tree)
print(dp)


#Define a function that takes a parse tree, and returns the position of the object DP if one exists, and None otherwise
def get_object_pos(tree):
    VP_pos = (-1,)
    for node in tree.treepositions(order="preorder"):
        if isinstance(tree[node], nltk.Tree): #Check if node has children
            if tree[node].label() == "VP":
                VP_pos = node
            if node[:len(VP_pos)] == VP_pos and tree[node].label() == "DP":
                return node

sentence = sentences[0]
parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                  
tokens = sentence.lower().split()
parse_tree = list(parser.parse(tokens))[0]
parse_tree.pretty_print()
obj = get_object_pos(parse_tree)
print(obj)

# %% [markdown]
# Assignment 3

# %%
translations = { 
    'John sees Mary' : 'SEES(j,m)', 
    'A student walks': 'some x [WALK(x)]', 
    'Some girl sees every boy': 'all y some x [(GIRL(x) ∧ BOY(y)) → SEES(x, y))]',
    'Every eager student passed': ''}

# %% [markdown]
# Assignment 4

# %%
vocabulary = {
    'P': (
        'with',
        'in',
        'on',
        'to',
        'without',
        'from'
    ),
    'C': (
        'that'
    ),
    'N': (
        'boy',
        'student',
        'girl',
        'class',
        'book',
        'teacher'
    ),
    'PropN': (
        'john',
        'mary'
    ),
    'Trace_e': (
        't1',
        't2',
        't3'
    ),
    'Trace_t': (
        't1',
        't2',
        't3'
    ),
    'Vi': (
        'walks',
        'passed'
        't_verb'
    ),
    'Vt': (
        'sees',
        'teaches'
    ),
    'Vpro': (
        'thinks',
        'believes'
    ),
    'Adj': (
        'eager',
        'smart'
    ),
    'Adv': (
        'eagerly',
        'well'
    ),
    'Det': (
        'a',
        'an',
        'the',
        'every',
        'some',
        'any'
    ),
    'Conj': (
        'and',
        'or',
        'but'
    )
}



# %% [markdown]
# Assignment 5

# %%
# this class would create an object storing both the representation of an element, and its typing information
class Formalization:
    def __init__(self, formula, type_hint, type_=None):
        self.formula = formula
        self.type = type_hint
        self.t = type_
        if type(type_hint) == tuple:
            self.selected = type_hint[0]
            self.returned = type_hint[1]
        else:
            self.selected = None

    def application(self, argument):
        if argument.type == self.selected:
            resulting_formula = self.formula(argument.formula)
            return Formalization(resulting_formula, self.returned, self.t)


# this dictionary contains functions to generate lexical entries for different parts of speech.
formalizations = {
    'PropN': lambda name: Formalization(
        name,
        'e', 'PropN'
    ),
    'Trace_e': lambda trace: Formalization(
        trace,
        'e', 'Trace_e'
    ),
    'Trace_t': lambda trace: Formalization(
        trace,
        't', 'Trace_t'
    ),
    'N': lambda noun: Formalization(
        lambda x: f'{noun.upper()}({x})',
        ('e', 't'), 'N'
    ),
    'Vi': lambda verb: Formalization(
        lambda x: f'{verb.upper()}({x})',
        ('e', 't'), 'Vi'
    ),
    'Vt': lambda verb: Formalization(
        lambda y: lambda x: f'{verb.upper()}({x}, {y})',
        ('e', ('e', 't')), 'Vt'
    ),
    'Vpro': lambda verb: Formalization(
        lambda P: lambda x: f'{verb.upper()}({x}, {P})',
        ('t', ('e','t')), 'Vpro'
    ),
    'Adj': lambda adjective: Formalization(
        lambda P: lambda x: f'{adjective.upper()}({x}) ^ {P(x)}',
        (('e', 't'), ('e', 't')), 'Adj'
    ),
    'Adv': lambda adverb: Formalization(
        lambda P: lambda x: f'{adverb.upper()}({P(x)})',
        (('e', 't'), ('e', 't')), 'Adv'
    ),
    'P': lambda preposition: Formalization(
        lambda x: lambda y: f'{preposition.upper()}({x}, {y})',
        ('e', ('e', 't')), 'P'
    ),
    'C': lambda preposition: Formalization(
        lambda P: f'({P})',
        ('t', 't'), 'C'
    ),
    'existential': lambda _: Formalization(
        lambda P: lambda Q: f'Exists x[{P("x")} ^ {Q("x")}]',
        (('e', 't'), (('e', 't'), 't')), 'existential'
    ),
    'universal': lambda _: Formalization(
        lambda P: lambda Q: f'All x[{P("x")} -> {Q("x")}]',
        (('e', 't'), (('e', 't'), 't')), 'universal'
    )
}


def generate_lexicon(vocab, translations):
    lexicon = {}
    for part_of_speech, entries in vocab.items():
        if part_of_speech in translations.keys():
            lexicon.update({part_of_speech: {word: translations[part_of_speech](word) for word in entries}})
        elif type(entries) == dict:
            lexicon[part_of_speech] = {}
            for subtype, words in entries.items():
                lexicon[part_of_speech].update({word: translations[subtype](word) for word in words})
        else:
            lexicon.update({part_of_speech: {word: Formalization(word, 'e') for word in entries}})
    return lexicon


def lexicon_to_terminals(lexicon):
    terminal_rules = ''
    for part_of_speech in lexicon.keys():
        terminals_string = " | ".join(["'" + word + "'" for word in lexicon[part_of_speech].keys()])
        terminal_rules += (part_of_speech + ' -> ' + terminals_string + '\n\t')
    return terminal_rules


extensional_lexicon = generate_lexicon(vocabulary, formalizations)

terminals_entries = lexicon_to_terminals(extensional_lexicon)

extensional_grammar = f"""
    S -> NP VP | Trace_e VP
    NP -> Det Nom | PropN | Trace_e
    Nom -> N  | Adj Nom | Nom PP
    VP -> Vi | Vt | Vpro | Vbar NP | Vbar NP PP | Adv VP | VP Adv | VP Conj VP | V AdvP | Vbar Trace_e | Vbar Trace_t | Vbar CP
    Vbar -> Vi | Vt | Vpro
    CP -> C Cbar
    Cbar -> NP VP
    AdvP -> Adv P
    PP -> P NP
    {terminals_entries}
"""

# %%
sentence = sentences[2]
parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                  
tokens = sentence.lower().split()
parse_tree = list(parser.parse(tokens))[0]
parse_tree.pretty_print()

# %%
for node in parse_tree.treepositions(order='postorder'):
    print(parse_tree[node], node)

# %% [markdown]
# Assignment 6

# %%
existentials = ['a', 'some', 'an']
universal = ['every']

def check_quantificational_children(result, node):
    return result[node + (1,)].t in ['existential', 'universal'] or result[node + (0,)].t in ['existential', 'universal']

def translate_to_logic(tree = nltk.Tree):
    result = {}
    prev_was_leave = False
    leaf = ''
    root_cause = None
    for node in tree.treepositions(order='postorder'):
        if isinstance(tree[node], nltk.Tree):
            if len(tree[node]) > 1:
                if tree[node].label() == 'S':
                    if check_quantificational_children(result, node):
                        print("help")
                        result[node] = result[node + (0,)].application(result[node + (1,)])
                    else:
                        print(result[node + (0,)])
                        result[node] = result[node + (1,)].application(result[node + (0,)])
                else:
                    result[node] = result[node + (0,)].application(result[node + (1,)])
                    if tree[node].label() == 'VP' and check_quantificational_children(result, node):
                        return None
            else:
                if prev_was_leave:
                    if leaf in existentials:
                        applier = 'existential'
                    elif leaf in universal:
                        applier = 'universal'
                    else:
                        applier = tree[node].label()
                    result[node] = formalizations[applier](leaf)
                    root_cause = result[node]
                    prev_was_leave = False
                else:
                    result[node] = root_cause
        else:
            prev_was_leave = True
            leaf = tree[node]
    return result
sentence = sentences[1]
parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                  
tokens = sentence.lower().split()
parse_tree = list(parser.parse(tokens))[0]
parse_tree.pretty_print()
res = translate_to_logic(parse_tree)
res[()].formula

# %%
res

# %%
[print(r.type, r.formula, k) for k, r in res.items() if r is not None]

# %% [markdown]
# Assignment 7 (Marloes)

# %%
def quantifier_raising(tree, nb, position):
    tree_ = tree.copy(deep=True)
    for i in range(nb-1):
        newposition = (1,) + position 
        position = newposition
        # print(f'the position is {position}')
    
    qp = tree_[position]
    tree_[position] = Tree('DP', [Tree('Trace_e', [f't{nb}'])])
    # print('after trace added \n')
    # tree_.pretty_print()

    tree_ = nltk.Tree(f'S{nb}',[qp, tree_])
    tree_[0].set_label(f'DP{nb}')
    return tree_


def raiser(tree=nltk.Tree):
    tree_list = []
    tree1 = tree.copy(deep=True)
    quant_dict = {}
    for node in tree1.treepositions(order='postorder'):
        if (tree1[node] in existentials) or (tree1[node] in universal):
            quant_dict[node[:-2]] = tree1[node[:-2]]
    # print(quant_dict)
    nb = 0
    # print('First Version \n')
    for key in quant_dict.keys():
        #print(quant_dict[key])
      
        nb += 1
        tree1 = quantifier_raising(tree1, nb, key)
        # tree1.pretty_print()
    tree_list.append(tree1)
    if len(quant_dict) == 2: # if there is another QP we will generate a new possible structure
        tree2 = tree.copy(deep=True)
        nb = 0
        # print('Second Version \n') 
        for key in reversed(quant_dict.keys()):
            # print(quant_dict[key])
            nb += 1
            tree2 = quantifier_raising(tree2, nb, key)
            # tree2.pretty_print()
    tree_list.append(tree2)
    return tree_list



## Assignment 8
def quantifier_logic(tree = nltk.Tree):
    traces = {}
    tree = tree.copy(deep=True)
    for node in tree.treepositions(order="postorder"):
        if isinstance(tree[node], nltk.Tree):
            if len(tree[node]) > 1:
                if tree[node].label() == 'S':
                    basic_tree = tree[node]
                    # print('basic tree:\n')
                    # basic_tree.pretty_print()
                    base_logic = translate_to_logic(basic_tree) # get the logcial form from below the raised quantifiers
                    # print(base_logic[()].formula)
            if tree[node].label() == 'Trace_e':
                traces[tree[node,0]] = node + (0,) # collect traces positions and names in a dictionary
    # print(traces)
    subtree_logic = {}
    for trace in traces.keys(): # now we will slowly do lambda abstraction per raised quantifier
        trace_number = trace[-1]
        for node in tree.treepositions(order="postorder"):
            if isinstance(tree[node], nltk.Tree):
                if len(tree[node]) > 1:
                    if tree[node].label() == f'DP{trace_number}':
                        subtree = tree[node].copy(deep=True)
                        subtree.set_label('DP')
                        sub_tree = nltk.Tree('S', [subtree, Tree('VP', [Tree('Vi', ['t_verb'])])]) # added a dummy verb because 
                                                                # the logic function does not like computing things without a verb
                        # sub_tree.pretty_print()
                        sub_logic = translate_to_logic(sub_tree)
                        # print(sub_logic[()].formula)
                        subtree_logic[trace] = sub_logic[()].formula

    # print(subtree_logic)

    variables = ['x','y','z']
    t = 0
    # trace_iteration = subtrees[list(subtrees.keys())[0]]
    new_logic = base_logic[()].formula

    for trace in subtree_logic.keys():
        subtree_logic[trace] = re.sub(r'(\W)x(\W)', '\\1'+variables[t]+'\\2', subtree_logic[trace])
        trace_logic = subtree_logic[trace]
        new_logic = re.sub(r'T_VERB\('+variables[t]+r'\)', new_logic, trace_logic) # fill predicate
        # print(new_logic)
        new_logic = re.sub(trace, variables[t], new_logic) # fill trace with variable
        t += 1
        # print(new_logic)
                        

        # lambda_abstraction = lambda trace: f'{base_logic}'
        # basically what I want to do here is have a variable (such as) 'x' replacing the position of trace in the base logic
        # result = sub_logic[()].application(base_logic[()]) # Not sure what I'm doing here tbh -> I want to apply the base logic to the quantifier phrase
        # print(result) # gives none
        # repeat for next trace -> have to make sure that we get a new variable for the next quantifier phrase (otherwise subject and object are referring to the same thing)
    logic = new_logic
    return logic

# sentence = sentences[2]
sentence = "a girl sees every boy"
parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                  
tokens = sentence.lower().split()
parse_tree = list(parser.parse(tokens))[0]
parse_tree.pretty_print()
parse_tree = raiser(parse_tree)[0]
print(quantifier_logic(parse_tree))

parse_tree = raiser(parse_tree)[1]
print(quantifier_logic(parse_tree))


######
# for translation to logic: translate up until first QP        ( SEE(t1,t2) )
# before QP apply lambda abstraction (lambda trace number)     ( lambda t1 SEE(t1,t2) )
# apply logical form QP to translation up till then ( (lambda Q some x[GIRL(x) ^ Q(x)] )(lambda t1 (SEE(t1, t2))) )
# give translation the variable that is inside QP () to fill lambda with (some x[GIRL(x)^(lambda t1 (SEE(t1, t2))) (x) ])
# fill up lambda trace: (some x[GIRL(x)^(SEE(x, t2))])
######
# repeat for next QP:
######
# lambda t2 some x[GIRL(x)^(SEE(x,t2))]
# (lambda Q all y[BOY(y) -> Q(y)]) (lambda t2 some x[GIRL(x)^(SEE(x,t2))])
# all y[BOY(y) -> (lambda t2 some x[GIRL(x)^(SEE(x,t2))])(y)]) 
# all y[BOY(y) -> some x[GIRL(x)^(SEE(x,y))] ])


# %% [markdown]
# Assignment 8 - Georgia and Marloes

# %%
# Assignment 8 - Marloes
def quantifier_logicG(tree = nltk.Tree):
    traces = {}
    treeq = tree.copy(deep=True)
    for node in tree.treepositions(order="postorder"):
        if isinstance(tree[node], nltk.Tree):
            if len(tree[node]) > 1:
                if tree[node].label() == 'S':
                    basic_tree = tree[node]
                    print('basic tree:\n')
                    basic_tree.pretty_print()
                    base_logic = translate_to_logic(basic_tree) # get the logcial form from below the raised quantifiers
                    print(base_logic[()].formula)
            if tree[node].label() == 'Trace':
                traces[tree[node,0]] = node + (0,) # collect traces positions and names in a dictionary
    print(traces)
    for trace in traces.keys(): # now we will slowly do lambda abstraction per raised quantifier
        trace_number = trace[-1]
        for node in tree.treepositions(order="postorder"):
            if isinstance(tree[node], nltk.Tree):
                if len(tree[node]) > 1:
                    if tree[node].label() == f'DP{trace_number}':
                        subtree = tree[node].copy(deep=True)
                        subtree.set_label('DP')
                        new_tree = nltk.Tree('S', [subtree])
                        sub_logic = translate_to_logic(subtree)
                        print(sub_logic[()].formula) # doesn't work?
                        new_tree.pretty_print()

        lambda_abstraction = lambda trace: f'{base_logic}'
        # basically what I want to do here is have a variable (such as) 'x' replacing the position of trace in the base logic
        
        result = sub_logic[()].application(base_logic[()]) # Not sure what I'm doing here tbh -> I want to apply the base logic to the quantifier phrase
        print(result) # gives none
    # repeat for next trace -> have to make sure that we get a new variable for the next quantifier phrase (otherwise subject and object are referring to the same thing)
    logic = ...
    return logic

sentence = sentences[2]
parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                  
tokens = sentence.lower().split()
parse_tree = list(parser.parse(tokens))[0]
parse_tree.pretty_print()
parse_tree = raiser(parse_tree)[0]

quantifier_logicG(parse_tree)


# %%
#Assignment 8 - Georgia

from itertools import permutations
import re

# check_quantificational_children
existentials = ['a', 'some', 'an']
universal = ['every']

def translate_to_logicG(tree = nltk.Tree): #Same function as the first one but this time with fixes for t1 and t2
    result = {}
    prev_was_leave = False
    leaf = ''
    root_cause = None
    for node in tree.treepositions(order='postorder'):
        if isinstance(tree[node], nltk.Tree):
            if len(tree[node]) > 1:
                if tree[node].label() == 'S':
                    if check_quantificational_children(result, node):
                        result[node] = result[node + (0,)].application(result[node + (1,)])
                    else:
                        result[node] = result[node + (1,)].application(result[node + (0,)])
                else:
                    if not isinstance(tree[node + (0,)], nltk.Tree): #If a t is in zero position apply flipped
                        if re.match(r't\d+', tree[node + (0,)]):
                            result[node] = result[node + (1,)].application(result[node + (0,)])
                    else:
                        result[node] = result[node + (0,)].application(result[node + (1,)])
                    if tree[node].label() == 'VP' and check_quantificational_children(result, node):
                        return None
            else:
                if prev_was_leave:
                    if leaf in existentials:
                        applier = 'existential'
                    elif leaf in universal:
                        applier = 'universal'
                    else:
                        applier = tree[node].label()
                    result[node] = formalizations[applier](leaf)
                    root_cause = result[node]
                    prev_was_leave = False
                elif not re.match(r"t\d+",leaf):
                    result[node] = root_cause
        else:
            prev_was_leave = True
            leaf = tree[node]
            if re.match(r"t\d+", leaf):
                result[node] = formalizations['PropN'](leaf)
    return result

def fix_root_system(tree): #Function to only make one node the S node and the sub nodes the S_sub
    for node in tree.treepositions('postorder'):
        if len(node) > 0 and isinstance(tree[node], nltk.Tree):
            if tree[node].label() == 'S':
                tree[node] = nltk.Tree('SUB_S', [n for n in tree[node]])
    return tree

def raise_node(tree = nltk.Tree, n_pos = tuple, replacement_='', new_label=''): #Raise a node to the top of the tree
    tree = tree.copy(deep=True)
    dp_pos = nltk.Tree(new_label, [n for n in tree[n_pos]])
    tree[n_pos] = replacement_
    return nltk.Tree('S',[dp_pos, tree])

def quantifier_possibilites(tree = nltk.Tree, by='DP'): #Calculate all possible trees for the translate to logic function
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

# parse_tree.pretty_print()
# tree = raise_node(parse_tree, (1,1), 't1', 'DP1')
# tree.pretty_print()
# tree = raise_node(tree, (1,0), 't2', 'DP2')
# tree.pretty_print()

sentence = sentences[2]
parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                  
tokens = sentence.lower().split()
parse_tree = list(parser.parse(tokens))[0]
parse_tree.pretty_print()
iterations = quantifier_possibilites(parse_tree)
iterations[0].pretty_print()
# print(translate_to_logicG(iterations[0])[(0,)].formula)




# %%


# %% [markdown]
# Assignment 10 - Daniel and Georgia

# %%


#modifying the LFs
event_grammar = nltk.CFG.fromstring("""
    EP -> Event VP
    ThetaP -> Role DP
    DP -> Det NP | NP | DP Conj DP
    NP -> N | PropN | Adj NP | NP PP
    VP -> ThetaP VP | Vi | Vt  | Vbar DP | Vbar DP PP | AdvP VP | VP Adv | VP Conj VP | V AdvP
    Vbar -> Vi | Vt
    AdvP -> Adv P
    PP -> P DP
    Det -> 'a' | 'an' | 'the' | 'every'| 'some' | 'any'
    P -> 'with' | 'in' | 'on' | 'to' | 'without' | 'from'
    Conj -> 'and' | 'or' | 'but'

    Event ->
    Role -> Agent | Patient
    N -> 'boy' | 'student' | 'girl' | 'class' | 'book' | 'teacher'
    PropN -> 'john' | 'mary'
    Adj -> 'eager' | 'smart'
    Vi -> 'walks' | 'passed' 
    Vt -> 'sees' | 'teaches'
    Adv -> 'eagerly' | 'well'
    
""")

# %% [markdown]
# Assignment 11 

# %% [markdown]
# **scope islands** 
# <!-- 
# # Main principles:
# - Every quantified phrase must properly bind a variable
# - Every variable in an argument position must be properly bound [c-commanded
# by a binding phrase]
# 
# - Island constraint 1: Following these conditions, quantifier phrases cannot be raised out of wh-phrases:
# - ∗Which man in some city did you meet?
# - [S’ [Which man in ti]j [S [some city]i [S did you meet tj]]]
# - First Quantifier Raising ([some city]i moves to higher S node)
# - Wh-phrase moves up (wh-movement) to S'
# - quantifier no longer c-commands variable
# - therefore the trace is no longer properly bound
# 
# - Everything can be summarized by the **Subjacency Condition**:
# - Move cannot relate two positions across two bounding notes. 
# - Bounding nodes are CP, TP, DP (when no complement of V)
# 
# # Examples:
# > Some man has met every cheer-leader.
# - There is a person who has met every single cheer-leader
# - For every cheer-leader, there is a man who has met them
# 
# > Some man regretted the fact that Bill had met every cheer-leader.
# Every cheer-leader cannot take scope over "some man" -> would imply moving over CP and TP (=2 bounding nodes) - complex noun phrase constraint
# - this means that we cannot derive the meaning: for every cheer-leader, there is a man who regrets that Bill has met them
# 
# same goes for:
# >  Someone believes that Mary is dating every student
# - cannot derive "for every student, there is someone who believes that Mary is dating them"
# - this is not due to subjacency condition (moves over TP but that is sister of DP, and then over another TP)
# - paper says: QR out of finite clauses is blocked
# 
# (https://www.ling.uni-potsdam.de/~zimmermann/teaching/Syntax-Semantic_Interface/Handouts/May-QuantifierRaising.pdf)
# 
# # Application
# - the easiest way to do this is I think to first try the quantifier raising, and then check if the QP is still c-commanding the trace
# - we can do this by going one level up from the QP node, then to the right and searching through that subtree to see if there is any trace with the same number
# 
# -->
# 
# - other method: 
# - "Every man thinks that some girl met every boy"
# - split up on "that" : `["Every man thinks", "some girl met every boy"]`
# - Derive logical forms:
# > all x [MAN(x) -> THINKS(x, P)]  (
# - t is trace for the object clause) -> **not intensional semantics proof**, but I think he'll forgive us
# > some y [GIRL(y) ^ all z[BOY(z) -> MET(y,z)]]
# > all z [BOY(z) -> some y[GIRL(y) ^ MET(y,z)]]
# 
# combined:
# 1. all x [MAN(x) -> THINKS(x, some y [GIRL(y) ^ all z[BOY(z) -> MET(y,z)]])]
# 2. all x [MAN(x) -> THINKS(x, all z [BOY(z) -> some y[GIRL(y) ^ MET(y,z)]])]
# 
# Formalization of "think":
# 
# think -> lambda x lambda P THINK(x, P)
# 
# `    'Vpro': lambda verb: Formalization(
#         lambda P: lambda x: f'{verb.upper()}({x}, {P})',
#         ('t', ('e', 't')), 'Vpro'
# ),
#         `
# 

# %% [markdown]
# Assignment 8 (version necessary for 11) Marloes + parts of Assignment 6

# %%
sentence = "a girl sees every boy"
parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                  
tokens = sentence.lower().split()
parse_tree = list(parser.parse(tokens))[0]
parse_tree.pretty_print()
parse_tree = raiser(parse_tree)[0]
print(quantifier_logic(parse_tree))

parse_tree = raiser(parse_tree)[1]
print(quantifier_logic(parse_tree))


######
# for translation to logic: translate up until first QP        ( SEE(t1,t2) )
# before QP apply lambda abstraction (lambda trace number)     ( lambda t1 SEE(t1,t2) )
# apply logical form QP to translation up till then ( (lambda Q some x[GIRL(x) ^ Q(x)] )(lambda t1 (SEE(t1, t2))) )
# give translation the variable that is inside QP () to fill lambda with (some x[GIRL(x)^(lambda t1 (SEE(t1, t2))) (x) ])
# fill up lambda trace: (some x[GIRL(x)^(SEE(x, t2))])
######
# repeat for next QP:
######
# lambda t2 some x[GIRL(x)^(SEE(x,t2))]
# (lambda Q all y[BOY(y) -> Q(y)]) (lambda t2 some x[GIRL(x)^(SEE(x,t2))])
# all y[BOY(y) -> (lambda t2 some x[GIRL(x)^(SEE(x,t2))])(y)]) 
# all y[BOY(y) -> some x[GIRL(x)^(SEE(x,y))] ])


# %%
# Island constraints: CP island

sentence = 'Some boy thinks that every boy sees some girl'
parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                  
tokens = sentence.lower().split()
parse_tree = list(parser.parse(tokens))[0]

parse_tree.pretty_print()

sub_trees = []
for subtree in parse_tree.subtrees():
    if subtree.label() == "CP" or subtree.label() == "Cbar":
        print(subtree.leaves())
        sub_trees.append(subtree)
# print(sub_trees)

basic_tree = parse_tree.copy(deep=True)

for node in basic_tree.treepositions(order = "postorder"):
    if isinstance(basic_tree[node], nltk.Tree):
            if len(basic_tree[node]) > 1:
                if basic_tree[node].label() == 'CP':
                    basic_tree[node] = nltk.Tree('DP',  [Tree('Trace_t', ['t1'])])

basic_tree.pretty_print()
res = translate_to_logic(basic_tree)  
main_logic = res[()].formula
print(main_logic)

if sub_trees[1]:
    sub_clause = sub_trees[1]
    sub_clause.set_label("S")

    sub_clause = raiser(sub_clause)[0] # I wanted to add a way to cycle through all possibilities but I couldn't manage in time
    sub_logic = quantifier_logic(sub_clause)

    print(sub_logic)
    sub_logic = re.sub(r'(\W)y(\W)', '\\1z\\2', sub_logic)
    sub_logic = re.sub(r'(\W)x(\W)', '\\1y\\2', sub_logic)


    full_logic = re.sub(r't1', f'({sub_logic})', main_logic)
else: 
     full_logic = main_logic

print(full_logic)




