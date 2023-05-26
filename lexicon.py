import re

# the words to use, sorted by parts of speech, subdivided where words of the same type need different formalizations
vocabulary = {
    'P': (
        'with',
        'in',
        'on',
        'to',
        'without',
        'from',
    ),
    'N': (
        'boy',
        'student',
        'girl',
        'class',
        'book',
        'teacher',
    ),
    'PropN': (
        'john',
        'mary',
    ),
    'Vi': (
        'walks',
        'passed',
    ),
    'Vt': (
        'sees',
        'teaches',
    ),
    'Vpro': (
        'think',
    ),
    'Adj': (
        'eager',
        'smart',
    ),
    'Adv': (
        'eagerly',
        'well',
    ),
    'Det': {
        'existential': (
            'a',
            'an',
            'the',
            'some'),
        'universal': (
            'every',
            'any',
        )
    },
    'Conj': (
        'and',
        'or',
        'but',
    ),
    'Role': (
        'agent',
        'patient'
    ),
    'Event': (
        'ev_exists',
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
                type_hint=argument.returned,
                formula_string=resulting_string
            )
        # case where there are two predicates, expected in event semantics
        elif (self.type == ('e', 't')) and (argument.type == ('e', 't')):
            resulting_formula = lambda x: f'{argument.formula(x)} ^ {self.formula(x)}'
            resulting_string = f'<lambda x: {argument.string}(_x_) ^ {self.string}(_x_)>'
            return Formalization(
                formula=resulting_formula,
                type_hint=('e', 't'),
                formula_string=resulting_string
            )
        else:
            print('type mismatch')

    def intensional_application(self, argument):
        if argument.type == self.returned[0]:  # that is, it matches what is selected by the extension
            resulting_formula = lambda w: self.formula(w)(argument.formula)
            resulting_string = combine_function_strings(combine_function_strings(self.string, '_w_'), argument.string)
            resulting_string = '<lambda w: ' + resulting_string + '>'
            return Formalization(
                formula=resulting_formula,
                type_hint=('s', self.returned[1]),
                formula_string=resulting_string
            )
        elif argument.returned[0] == self.type:
            resulting_formula = lambda w: argument.formula(w)(self.formula)
            resulting_string = combine_function_strings(combine_function_strings(argument.string, '_w_'), self.string)
            resulting_string = '<lambda w: ' + resulting_string + '>'
            return Formalization(
                formula=resulting_formula,
                type_hint=('s', argument.returned[1]),
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
    'Vpro': lambda verb: Formalization(
        lambda P: lambda x: f'{verb.upper()}({x}, {P})',
        ('t', ('e', 't')),
        'Vpro',
        f'<lambda P: <lambda x: {verb.upper()}(_x_, _P_)'
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
    # 'existential': lambda _: Formalization(
    #     lambda P: lambda Q: f'Exists x[{P("x")} ^ {Q("x")}]',
    #     (('e', 't'), (('e', 't'), 't')),
    #     'existential',
    #     '<lambda P: <lambda Q: Exists x[_P_(x) ^ _Q_(x)]>>'
    # ),
    # 'universal': lambda _: Formalization(
    #     lambda P: lambda Q: f'All x[{P("x")} -> {Q("x")}]',
    #     (('e', 't'), (('e', 't'), 't')),
    #     'universal',
    #     '<lambda P: <lambda Q: All x[_P_(x) -> _Q_(x)]>>'
    # ),
    # alternative entry for quantifiers where they can use variables represented by other things than x
    'existential': lambda _: Formalization(
        lambda v: lambda P: lambda Q: f'Exists {v}[{P(v)} ^ {Q(v)}]',
        ('v', (('e', 't'), (('e', 't'), 't'))),
        'existential',
        '<lambda v : <lambda P: <lambda Q: Exists _v_[_P_(_v_) ^ _Q_(_v_)]>>>'
    ),
    'universal': lambda _: Formalization(
        lambda v: lambda P: lambda Q: f'All {v}[{P(v)} -> {Q(v)}]',
        ('v', (('e', 't'), (('e', 't'), 't'))),
        'universal',
        '<lambda v : <lambda P: <lambda Q: All _v_[_P_(_v_) -> _Q_(_v_)]>>>'
    ),
    'Var': lambda name: Formalization(
        name,
        'v',
        'Var',
        name,
    ),
}

formalizations_events = formalizations.copy()
formalizations_events.update({
    'Vi': lambda verb: Formalization(
        lambda e: f'{verb.upper()}({e})',
        ('e', 't'),
        'Vi',
        f'<lambda e: {verb.upper()}(_e_)>'
    ),
    'Vt': lambda verb: Formalization(
        lambda e: f'{verb.upper()}({e})',
        ('e', 't'),
        'Vt',
        f'<lambda e: {verb.upper()}(_e_)>'
    ),
    'Adv': lambda adverb: Formalization(
        lambda e: f'{adverb.upper()}({e})',
        ('e', 't'),
        'Adv',
        f'<lambda e: {adverb.upper()}(_e_)>'
    ),
    'Role': lambda role: Formalization(
        lambda x: lambda e: f'{role.upper()}({x}, {e})',
        ('e', ('e', 't')),
        'Role',
        f'<lambda x: <lambda e: {role.upper()}(_x_, _e_)>>'
    ),
    'Event': lambda _: Formalization(
        lambda P: f'Exists e[{P("e")}]',
        (('e', 't'), 't'),
        'Event',
        f'<lambda P: Exists e[_P_(e)]>'
    )
})

intensional_formalizations = {
    'PropN': lambda name: Formalization(
        lambda w: name,
        ('s', 'e'),
        'PropN',
        f'<lambda w: {name}>'
    ),
    'N': lambda noun: Formalization(
        lambda w: lambda x: f'{noun.upper()}({w})({x(w)})',
        ('s', (('s', 'e'), 't')),
        'N',
        f'<lambda w: <lambda x: {noun.upper()}(_w_)(_x_(_w_))>>'
    ),
    'Vi': lambda verb: Formalization(
        lambda w: lambda x: f'{verb.upper()}({w})({x(w)})',
        ('s', (('s', 'e'), 't')),
        'N',
        f'<lambda w: <lambda x: {verb.upper()}(_w_)(_x_(_w_))>>'
    ),
    'Vt': lambda verb: Formalization(
        lambda w: lambda y: lambda x: f'{verb.upper()}({w})({x(w)}, {y(w)})',
        ('s', (('s', 'e'), (('s', 'e'), 't'))),
        'Vt',
        f'<lambda w: <lambda y: <lambda x: {verb.upper()}(_w_)(_x_(_w_), _y_(_w_))>>>'
    ),
    'Adj': lambda adjective: Formalization(
        lambda w: lambda P: lambda x: f'{adjective.upper()}({w})({x(w)}) ^ {P(w)(x(w))}',
        ('s', ((('s', 'e'), 't'), (('s', 'e'), 't'))),
        'Adj',
        f'<lambda w: <lambda P: <lambda x: {adjective.upper()}(_w_)(_x_(_w_)) ^ _P_(_w_)(_x_(_w_))>>>'
    ),
    'Adv': lambda adverb: Formalization(
        lambda w: lambda P: lambda x: f'{adverb.upper()}({w})({P(w)(x(w))})',
        ('s', ((('s', 'e'), 't'), (('s', 'e'), 't'))),
        'Adv',
        f'<lambda P: <lambda x: {adverb.upper()}(_w_)(_P_(_w_)(_x_(_w_)))>>'
    ),
    'P': lambda preposition: Formalization(
        lambda w: lambda y: lambda x: f'{preposition.upper()}({w})({x(w)}, {y(w)})',
        ('s', (('s', 'e'), (('s', 'e'), 't'))),
        'P',
        f'<lambda w: <lambda y: <lambda x: {preposition.upper()}(_w_)(_x_(_w_), _y_(_w_))>>>'
    ),
    # Predicate intension functions will attempt to call their argument, so quantifiers look like this now
    'existential': lambda _: Formalization(
        lambda w: lambda P: lambda Q: f'Exists x[{P(w)(lambda _: "x")} ^ {Q(w)(lambda _: "x")}]',
        ('s', (('s', (('s', 'e'), 't')), (('s', (('s', 'e'), 't')), 't'))),
        'existential',
        '<lambda w: <lambda P: <lambda Q: Exists x[_P_(_w_)(x) ^ _Q_(_w_)(x)]>>>'
    ),
    'universal': lambda _: Formalization(
        lambda w: lambda P: lambda Q: f'All x[{P(w)(lambda _: "x")} -> {Q(w)(lambda _: "x")}]',
        ('s', (('s', (('s', 'e'), 't')), (('s', (('s', 'e'), 't')), 't'))),
        'universal',
        '<lambda w: <lambda P: <lambda Q: All x[_P_(_w_)(x) -> _Q_(_w_)(x)]>>>'
    )
}


# takes a vocabulary and a dictionary of translation methods,
# then returns a lexicon storing word: Formalization pairs sorted by parts of speech
def generate_lexicon(vocab, translations):
    lexicon = {}
    for part_of_speech, entries in vocab.items():
        if part_of_speech in translations.keys():
            lexicon.update({word: translations[part_of_speech](word) for word in entries})
        elif type(entries) == dict:
            for subtype, words in entries.items():
                lexicon.update({word: translations[subtype](word) for word in words})
        else:
            lexicon.update({part_of_speech: {word: Formalization(word, 'e') for word in entries}})
    return lexicon


# generate entries for terminal symbol rules for use in grammar based on a lexicon as created by generate_lexicon
def vocabulary_to_terminals(vocab):
    terminal_rules = ''
    for part_of_speech in vocab.keys():
        if type(vocab[part_of_speech]) == dict:
            words = ()
            for sublist in vocab[part_of_speech].values():
                words += tuple(word for word in sublist)
        else:
            words = vocab[part_of_speech]
        terminals_string = " | ".join(["'" + word + "'" for word in words])
        terminal_rules += (part_of_speech + ' -> ' + terminals_string + '\n\t')
    return terminal_rules


extensional_lexicon = generate_lexicon(vocabulary, formalizations)
intensional_lexicon = generate_lexicon(vocabulary, intensional_formalizations)
event_lexicon = generate_lexicon(vocabulary, formalizations_events)

extensional_grammar = f"""
    S -> DP VP
    DP -> Det NP | PropN
    NP -> N  | Adj NP | NP PP
    VP -> Vi | Vt  | Vbar DP | Vbar DP PP | Adv VP | VP Adv | VP Conj VP | V AdvP
    Vbar -> Vi | Vt
    AdvP -> Adv P
    PP -> P DP
    
    {vocabulary_to_terminals(vocabulary)}
"""

event_grammar = f"""
    EP -> Event VP
    ThetaP -> Role DP
    DP -> Det NP | NP | DP Conj DP
    NP -> N | PropN | Adj NP | NP PP
    VP -> ThetaP VP | Vi | Vt | Vbar ThetaP | Vbar ThetaP PP | AdvP VP | VP Adv | VP Conj VP | V AdvP
    Vbar -> Vi | Vt
    AdvP -> Adv P
    PP -> P DP
    
    {vocabulary_to_terminals(vocabulary)}
"""
# # for testing purposes
# print(event_lexicon)
# print(extensional_grammar)

# result = extensional_lexicon['Det']['every'].application(
#     extensional_lexicon['N']['student']
# ).application(
#     extensional_lexicon['Vi']['passed']
# )
# print(result.string)
