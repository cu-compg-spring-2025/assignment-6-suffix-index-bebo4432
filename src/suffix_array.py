import argparse
import utils
import suffix_tree

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

def build_suffix_array(T):
    tree = suffix_tree.build_suffix_tree(T)
    suf_array = []
    stack = [(0, 0)]  # (node idx, depth)
    while stack:
        node_idx, depth = stack.pop()
        node = tree[node_idx]
        if not node[CHILDREN]:
            suffix_idx = len(T) - depth
            if suffix_idx >= 0:  # Ensure valid index
                suf_array.append(suffix_idx)
        for child in node[CHILDREN].values():
            stack.append((child, depth + len(tree[child][SUB])))
    return sorted(suf_array)

def compare_suffix(T, suffix_idx, q):
    i = 0
    while i < len(q) and suffix_idx + i < len(T) and T[suffix_idx + i] == q[i]:
        i += 1
    return i

def search_array(T, suffix_array, q):
    lo = 0
    hi = len(suffix_array)
    best_match_len = 0
    
    # Modified binary search
    while lo < hi:
        mid = (lo + hi) // 2
        suffix_idx = suffix_array[mid]
        match_len = compare_suffix(T, suffix_idx, q)
        if match_len == len(q) or (suffix_idx + match_len < len(T) and T[suffix_idx + match_len] > q[match_len]):
            hi = mid
        else:
            lo = mid + 1
            
        best_match_len = max(best_match_len, match_len)
    return best_match_len

def main():
    args = get_args()

    T = None

    if args.string:
        T = args.string
    elif args.reference:
        reference = utils.read_fasta(args.reference)
        T = reference[0][1]

    array = build_suffix_array(T)

    if args.query:
        for query in args.query:
            match_len = search_array(T, array, query)
            print(f'{query} : {match_len}')

if __name__ == '__main__':
    main()