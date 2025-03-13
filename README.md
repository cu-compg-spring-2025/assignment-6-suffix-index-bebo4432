[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/2H4hMYgM)

# suffix_index
Suffix data structures for aligning reads to a reference.

## Suffix Array

### `build_suffix_array(text)`

#### Purpose
The `build_suffix_array` function constructs a suffix array for a given input string `text`.

#### Parameters
- `text`: The input string for which the suffix array is to be constructed.

#### Returns
A list of integers representing the starting indices of the suffixes of `text` in lexicographical order.

#### Operation
- Generates all suffixes of `text` along with their starting indices.
- Sorts the suffixes lexicographically.
- Returns the list of starting indices of the sorted suffixes.

### `search_array(text, suffix_array, pattern)`

#### Purpose
The `search_array` function searches for a pattern in the text using the suffix array.

#### Parameters
- `text`: The input string in which to search for the pattern.
- `suffix_array`: The suffix array of the input string.
- `pattern`: The pattern to search for.

#### Returns
A list of starting indices where the pattern is found in the text.

## Suffix Trie

### `build_suffix_trie(text)`

#### Purpose
The `build_suffix_trie` function constructs a suffix trie for a given input string `text`.

#### Parameters
- `text`: The input string for which the suffix trie is to be constructed.

#### Returns
A trie data structure representing all suffixes of the input string.

### `search_trie(trie, pattern)`

#### Purpose
The `search_trie` function searches for a pattern in the text using the suffix trie.

#### Parameters
- `trie`: The suffix trie of the input string.
- `pattern`: The pattern to search for.

#### Returns
A list of starting indices where the pattern is found in the text.

## Suffix Tree

### `add_suffix(nodes, suf)`

#### Purpose
The `add_suffix` function integrates a suffix `suf` into an existing tree structure represented by nodes.

#### Parameters
- `nodes`: A list of nodes representing the current state of the suffix tree.
- `suf`: A string representing the suffix to be added to the suffix tree.

#### Operation
- Iterates over the characters of `suf`.
- Checks if the character is already represented in the tree at the current node's children.
- If not, creates a new node for the remaining part of `suf`.
- If found, compares the suffix with the substring of the found node to check how much of it matches.
- If a mismatch is found, creates a new intermediate node to represent the common prefix and splits the original node.

### `build_suffix_tree(text)`

#### Purpose
The `build_suffix_tree` function constructs a suffix tree for a given input string `text`.

#### Parameters
- `text`: The input string for which the suffix tree is to be constructed.

#### Returns
A list of nodes representing the suffix tree of the input text.

#### Operation
- Appends a terminal symbol `$` to the end of `text`.
- Initializes the tree with a single root node.
- Iterates over each index of `text`, treating each suffix as a new suffix to be added to the tree.
- Calls `add_suffix` for each suffix.
- Returns the constructed suffix tree.

### `search_tree(tree, pattern)`

#### Purpose
The `search_tree` function searches for a pattern in the text using the suffix tree.

#### Parameters
- `tree`: The suffix tree of the input string.
- `pattern`: The pattern to search for.

#### Returns
A list of starting indices where the pattern is found in the text.

## Experiments

### Purpose
The experiments measure the search times for different patterns using the three data structures (Suffix Array, Suffix Trie, and Suffix Tree) and plot the distribution of search times.

### Running the Experiments
1. Ensure you have the required data files in the `data` folder.
2. Run the `run_experiments.py` script to perform the experiments and generate the plots.

```bash
python src/run_experiments.py