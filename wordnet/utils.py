import argparse

from nltk.corpus import wordnet as wn


def get_wnid(term):
    assert isinstance(term, str), "Must pass string"
    syns = wn.synsets(term.lower())
    syn = syns.pop(0)
    print("{}\nDefinition: {}".format(term.capitalize(), syn.definition()))

    wnid = syn.offset()

    return wnid


if __name__ == "__main__":
    wnid = get_wnid('dog')
    print("WNID:", wnid)
