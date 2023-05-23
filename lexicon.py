import re

# the words to use, sorted by parts of speech, subdivided where words of the same type need different formalizations
vocabulary = {
    'P': (
        'with',
        'in',
        'on',
        'to',
        'without',
        'from'
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
    'Vi': (
        'walks',
        'passed'
    ),
    'Vt': (
        'sees',
        'teaches'
    ),
    'Adj': (
        'eager',
        'smart'
    ),
    'Adv': (
        'eagerly',
        'well'
    ),
    'Det': {
        'existential': (
            'a',
            'an',
            'the',
            'some'),
        'universal': (
            'every',
            'any'
        )
    },
    'Conj': (
        'and',
        'or',
        'but'
    )
}


# a function that takes string representations of functions and combines them
def combine_function_strings(f1, f2):
    var_to_swap = f1[8]  # find what symbol to substitute, formulas have form <lambda s : rest>
    full_function = f1[11:-1].replace(f'_{var_to_swap}_', f2)  # remove brackets and substitute variables, marked _v_
    # print('full', full_function)
    while True:
        # find cases for simplification. does not catch cases where function contains unresolved functions,
        # or argument contains parentheses
        stuff_to_simplify = re.search(r'<[^<>]*>\([^()]*\)', full_function)
        if stuff_to_simplify:
            stuff_to_simplify = stuff_to_simplify[0]  # retrieve the actual string
            # print('to simplify', stuff_to_simplify)
            function_part = re.search(r'<[^<>]*>\(', stuff_to_simplify)[0][:-1]
            # print('fun', function_part)
            argument_part = stuff_to_simplify.replace(function_part, '')[1:-1]  # cut the parentheses
            # print('arg', argument_part)
            replacement = combine_function_strings(
                function_part,
                argument_part
            )
            full_function = full_function.replace(stuff_to_simplify, replacement)
        else:
            break  # exit once no simplifications can be made
    # print('simplified', full_function)
    return full_function


# this class creates an object storing both the representation of an element, and its typing information
class Formalization:
    def __init__(self, formula, type_hint, type_=None, formula_string=''):
        self.formula = formula
        self.type = type_hint
        self.t = type_
        self.string = formula_string
        if type(type_hint) == tuple:
            self.selected = type_hint[0]
            self.returned = type_hint[1]
        else:
            self.selected = None

    # take another formalization object and try to compose them into a new object
    def application(self, argument):
        if argument.type == self.selected:
            resulting_formula = self.formula(argument.formula)
            resulting_string = combine_function_strings(self.string, argument.string)
            return Formalization(
                formula=resulting_formula,
                type_hint=self.returned,
                formula_string=resulting_string
            )
        elif self.type == argument.selected:
            resulting_formula = argument.formula(self.formula)
            resulting_string = combine_function_strings(argument.string, self.string)
            return Formalization(
                formula=resulting_formula,
                type_hint=self.returned,
                formula_string=resulting_string
            )
        else:
            print('type mismatch')

    # create an object where a given trace string is replaced by a variable
    def remove_traces(self, trace):
        split_formula = self.formula.split(trace)
        new_formula = lambda x: f'{x}'.join(split_formula)
        split_string = self.string.split(trace)
        new_string = '<lambda x:' + 'x'.join(split_string) + '>'
        return Formalization(
            formula=new_formula,
            type_hint=('e', self.type),
            formula_string=new_string
        )


# this dictionary contains functions to generate lexical entries for different parts of speech.
formalizations = {
    'PropN': lambda name: Formalization(
        name,
        'e',
        'PropN',
        name
    ),
    'N': lambda noun: Formalization(
        lambda x: f'{noun.upper()}({x})',
        ('e', 't'),
        'N',
        f'<lambda x: {noun.upper()}(_x_)>'
    ),
    'Vi': lambda verb: Formalization(
        lambda x: f'{verb.upper()}({x})',
        ('e', 't'),
        'Vi',
        f'<lambda x: {verb.upper()}(_x_)>'
    ),
    'Vt': lambda verb: Formalization(
        lambda y: lambda x: f'{verb.upper()}({x}, {y})',
        ('e', ('e', 't')),
        'Vt',
        f'<lambda y: <lambda x: {verb.upper()}(_x_, _y_)>>'
    ),
    'Adj': lambda adjective: Formalization(
        lambda P: lambda x: f'{adjective.upper()}({x}) ^ {P(x)}',
        (('e', 't'), ('e', 't')),
        'Adj',
        f'<lambda P: <lambda x: {adjective.upper()}(_x_) ^ _P_(_x_)>>'
    ),
    'Adv': lambda adverb: Formalization(
        lambda P: lambda x: f'{adverb.upper()}({P(x)})',
        (('e', 't'), ('e', 't')),
        'Adv',
        f'<lambda P: <lambda x: {adverb.upper()}(_P_(_x_))>>'
    ),
    'P': lambda preposition: Formalization(
        lambda x: lambda y: f'{preposition.upper()}({x}, {y})',
        ('e', ('e', 't')),
        'P',
        f'<lambda y: <lambda x: {preposition.upper()}(_x_, _y_)>>'
    ),
    'existential': lambda _: Formalization(
        lambda P: lambda Q: f'Exists x[{P("x")} ^ {Q("x")}]',
        (('e', 't'), (('e', 't'), 't')),
        'existential',
        '<lambda P: <lambda Q: Exists x[_P_(x) ^ _Q_(x)]>>'
    ),
    'universal': lambda _: Formalization(
        lambda P: lambda Q: f'All x[{P("x")} -> {Q("x")}]',
        (('e', 't'), (('e', 't'), 't')),
        'universal',
        '<lambda P: <lambda Q: All x[_P_(x) -> _Q_(x)]>>'
    ),
    # alternative entry for quantifiers where they can use variables represented by other things than x
    # 'existential': lambda _: Formalization(
    #     lambda v: lambda P: lambda Q: f'Exists {v}[{P({v})} ^ {Q({v})}]',
    #     (('e', 't'), (('e', 't'), 't')),
    #     'existential',
    #     '<lambda v : <lambda P: <lambda Q: Exists v[_P_(v) ^ _Q_(v)]>>>'
    # ),
    # 'universal': lambda _: Formalization(
    #     lambda v: lambda P: lambda Q: f'All {v}[{P({v})} -> {Q({v})}]',
    #     (('e', 't'), (('e', 't'), 't')),
    #     'universal',
    #     '<lambda v : <lambda P: <lambda Q: All v[_P_(v) -> _Q_(v)]>>>'
    # )
}


# takes a vocabulary and a dictionary of translation methods,
# then returns a lexicon storing word: Formalization pairs sorted by parts of speech
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


# generate entries for terminal symbol rules for use in grammar based on a lexicon as created by generate_lexicon
def lexicon_to_terminals(lexicon):
    terminal_rules = ''
    for part_of_speech in lexicon.keys():
        terminals_string = " | ".join(["'" + word + "'" for word in lexicon[part_of_speech].keys()])
        terminal_rules += (part_of_speech + ' -> ' + terminals_string + '\n\t')
    return terminal_rules


extensional_lexicon = generate_lexicon(vocabulary, formalizations)

terminals_entries = lexicon_to_terminals(extensional_lexicon)

extensional_grammar = f"""
    S -> NP VP
    NP -> Det Nom | PropN
    Nom -> N  | Adj Nom | Nom PP
    VP -> Vi | Vt  | Vbar NP | Vbar NP PP | Adv VP | VP Adv | VP Conj VP | V AdvP
    Vbar -> Vi | Vt
    AdvP -> Adv P
    PP -> P NP
    
    {terminals_entries}
"""

# # for testing purposes
# print(extensional_lexicon)
# print(extensional_grammar)

# result = extensional_lexicon['Det']['every'].application(
#     extensional_lexicon['N']['student']
# ).application(
#     extensional_lexicon['Vi']['passed']
# )
# print(result.string)
