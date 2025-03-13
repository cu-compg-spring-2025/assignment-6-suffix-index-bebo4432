import argparse
import utils

SUB = 0
CHILDREN = 1

def get_args():
    parser = argparse.ArgumentParser(description='Suffix Tree')

    parser.add_argument('--reference',
                        help='Reference sequence file',
                        type=str)

    parser.add_argument('--string',
                        help='Reference sequence',
                        type=str)

    parser.add_argument('--query',
                        help='Query sequences',
                        nargs='+',
                        type=str)

    return parser.parse_args()


def add_suffix(nodes, suf):
    n = 0
    i = 0
    while i < len(suf):
        b = suf[i] 
        children = nodes[n][CHILDREN]
        if b not in children:
            n2 = len(nodes)
            nodes.append([suf[i:], {}])
            nodes[n][CHILDREN][b] = n2
            return
        else:
            n2 = children[b]

        sub2 = nodes[n2][SUB]
        j = 0
        while j < len(sub2) and i + j < len(suf) and suf[i + j] == sub2[j]:
            j += 1

        if j < len(sub2):
            n3 = n2 
            n2 = len(nodes)
            nodes.append([sub2[:j], {sub2[j]: n3}])
            nodes[n3][SUB] = sub2[j:]
            nodes[n][CHILDREN][b] = n2

        i += j
        n = n2

def build_suffix_tree(text):
    text += "$"

    nodes = [ ['', {}] ]

    for i in range(len(text)):
        add_suffix(nodes, text[i:])
    
    return nodes

def search_tree(suffix_tree, P):
    # Your code here
    i = 0
    j = 0
    while i < len(P):
        b = P[j]
        children = suffix_tree[i][CHILDREN]
        if b not in children:
            return i
        b2 = children[b]
        sub = suffix_tree[b2][SUB]
        k = 0
        while k < len(sub) and j + k < len(P) and P[j + k] == sub[k]:
            k += 1
        if k < len(sub):
            return j + k
        j += k
        i = b2
    return len(P)

def main():
    args = get_args()

    T = None

    if args.string:
        T = args.string
    elif args.reference:
        reference = utils.read_fasta(args.reference)
        T = reference[0][1]

    tree = build_suffix_tree(T)
        
    if args.query:
        for query in args.query:
            match_len = search_tree(tree, query)
            print(f'{query} : {match_len}')

if __name__ == '__main__':
    main()
