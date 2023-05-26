import nltk
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

# select the verb for the sentence 'john sees mary'
print(trees[0][1, 0])
# select the subject for the sentence 'john sees mary'
print(trees[0][0])
# select the determiner for sentence 'A student walks'
print(trees[1][0, 0])
print('\n')

# practice iterating
for sub in trees[2].subtrees():
    print(sub)
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
