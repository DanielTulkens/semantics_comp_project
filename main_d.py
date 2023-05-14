import nltk
grammar = nltk.CFG.fromstring("""
    <define grammar here>
    """)

parser = nltk.parse.RecursiveDescentParser(grammar)

sentence = "some girl saw every boy"
tokens = sentence.split()

parse_trees = parser.parse(tokens)

if not parse_trees:
    print("No parse tree found.")

for parse_tree in parse_trees:
    print(parse_tree)
