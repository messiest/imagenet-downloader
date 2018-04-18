import argparse

from nltk.corpus import wordnet as wn


def get_wnid(term):
    assert isinstance(term, str), "Must pass string"
    syns = wn.synsets(term.lower())
    syn = syns.pop(0)
    print("Definition:", syn.definition())

    wnid = syn.offset()

    return wnid


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "term",
        type=str,
    )
    args = parser.parse_args()
    term = args.term

    wnid = get_wnid(term)
    print("WNID:", wnid)
