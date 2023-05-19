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


# this class would create an object storing both the representation of an element, and its typing information
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


# this dictionary contains functions to generate lexical entries for different parts of speech.
formalizations = {
    'PropN': lambda name: Formalization(
        name,
        'e'
    ),
    'N': lambda noun: Formalization(
        lambda x: f'{noun.upper()}({x})',
        ('e', 't')
    ),
    'Vi': lambda verb: Formalization(
        lambda x: f'{verb.upper()}({x})',
        ('e', 't')
    ),
    'Vt': lambda verb: Formalization(
        lambda y: lambda x: f'{verb.upper()}({x}, {y})',
        ('e', ('e', 't'))
    ),
    'Adj': lambda adjective: Formalization(
        lambda P: lambda x: f'{adjective.upper()}({x}) ^ {P(x)}',
        (('e', 't'), ('e', 't'))
    ),
    'Adv': lambda adverb: Formalization(
        lambda P: lambda x: f'{adverb.upper()}({P(x)})',
        (('e', 't'), ('e', 't'))
    ),
    'P': lambda preposition: Formalization(
        lambda x: lambda y: f'{preposition.upper()}({x}, {y})',
        ('e', ('e', 't'))
    ),
    'existential': lambda _: Formalization(
        lambda P: lambda Q: f'Exists x[{P("x")} ^ {Q("x")}]',
        (('e', 't'), (('e', 't'), 't'))
    ),
    'universal': lambda _: Formalization(
        lambda P: lambda Q: f'All x[{P("x")} -> {Q("x")}]',
        (('e', 't'), (('e', 't'), 't'))
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
