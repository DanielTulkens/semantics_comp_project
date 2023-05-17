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


# this dictionary contains functions to generate lexical entries for different parts of speech.
# items denoting entities or truth values are represented as strings, other elements as anonymous functions
formalizations = {
    'PropN': lambda name: name,
    'N': lambda noun: lambda x: f'{noun}({x})',
    'Vi': lambda verb: lambda x: f'{verb}({x})',
    'Vt': lambda verb: lambda y: lambda x: f'{verb}({x}, {y})',
    'Adj': lambda adjective: lambda P: lambda x: f'{adjective}({x}) ^ {P(x)}',
    'Adv': lambda adverb: lambda P: lambda x: f'{adverb}({P(x)})'
}


class Formalization:
    def __init__(self, formula, type_hint):
        self.formula = formula
        self.type = type_hint
        if type(type_hint) == tuple:
            self.selected = type_hint[0]
            self.returned = type_hint[1]
        else:
            self.selected = None

    def application(self, argument):
        if argument.type == self.selected:
            resulting_formula = self.formula(argument.formula)
            return Formalization(resulting_formula, self.returned)


def generate_lexicon(vocab, translations):
    lexicon = {}
    for part_of_speech, entries in vocab.items():
        if part_of_speech in translations.keys():
            lexicon.update({part_of_speech: {word: translations[part_of_speech](word) for word in entries}})
        else:
            lexicon.update({part_of_speech: {word: word for word in entries}})
    return lexicon


def lexicon_to_terminals(lexicon):
    terminal_rules = ''
    for part_of_speech in lexicon.keys():
        terminals_string = " | ".join(["'" + word + "'" for word in lexicon[part_of_speech].keys()])
        terminal_rules += (part_of_speech + ' -> ' + terminals_string + '\n\t')
    return terminal_rules


extensional_lexicon = generate_lexicon(vocabulary, formalizations)

existential_quantifier = lambda P: lambda Q: f'Exists x[{P("x")} ^ {Q("x")}]'
universal_quantifier = lambda P: lambda Q: f'All x[{P("x")} -> {Q("x")}]'
definite_description = lambda P: lambda Q: f'Exists! x[{P("x")} ^ {Q("x")}]'

extensional_lexicon.update(
    {'Det': {
        'a': existential_quantifier,
        'an': existential_quantifier,
        'the': definite_description,
        'every': universal_quantifier,
        'some': existential_quantifier,
        'any': universal_quantifier,
    }}
)

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
