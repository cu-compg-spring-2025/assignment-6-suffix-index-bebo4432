import os
import time
import gzip
import matplotlib.pyplot as plt
from suffix_array import build_suffix_array, search_array
from suffix_trie import build_suffix_trie, search_trie
from suffix_tree import build_suffix_tree, search_tree

# Define the strings to test
test_strings = ['AA', 'AGTCCAG', 'ACATACTAGATCCACCA']

# Define the data files
data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
# print(f"Data folder: {data_folder}")  # Debug statement
data_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.fa.gz')]
# print(f"Data files: {data_files}")  # Debug statement

# Function to measure the time taken to search for a string in a data structure
def measure_time(search_function, *args):
    start_time = time.perf_counter()  # Use a higher precision timer
    search_function(*args)
    end_time = time.perf_counter()
    return end_time - start_time

# Function to run experiments
def run_experiments():
    results = { 'SuffixArray': [], 'SuffixTrie': [], 'SuffixTree': [] }

    for data_file in data_files:
        if 'chr22' in data_file:
            # print(f"Skipping file: {data_file}")  # Debug statement
            continue
        if 'kcnq2' in data_file:
            # print(f"Skipping file: {data_file}")
            continue

        # print(f"Processing file: {data_file}")  # Debug statement
        with gzip.open(data_file, 'rt') as file:
            # Skip the first line and read the next 1000 bases
            file.readline()  # Skip the first line
            data = file.read(1000)  # Read the next 1000 bases
            # print(f"Data read from file: {data[:50]}...")  # Debug statement to print the first 50 characters

        # Build data structures
        suffix_array = build_suffix_array(data)
        # print(f"Suffix Array: {suffix_array[:10]}...")  # Debug statement to print the first 10 elements
        suffix_trie = build_suffix_trie(data)
        # print(f"Suffix Trie: {suffix_trie}")  # Debug statement to print the trie
        suffix_tree = build_suffix_tree(data)
        # print(f"Suffix Tree: {suffix_tree}")  # Debug statement to print the tree

        for string in test_strings:
            # Measure search time for suffix array
            # print(f"Searching for '{string}' in Suffix Array...")
            time_suffix_array = measure_time(search_array, data, suffix_array, string)
            results['SuffixArray'].append((len(string), time_suffix_array))
            # print(f"SuffixArray search time for '{string}': {time_suffix_array}")  # Debug statement

            # Measure search time for suffix trie
            # print(f"Searching for '{string}' in Suffix Trie...")
            time_suffix_trie = measure_time(search_trie, suffix_trie, string)
            results['SuffixTrie'].append((len(string), time_suffix_trie))
            # print(f"SuffixTrie search time for '{string}': {time_suffix_trie}")  # Debug statement

            # Measure search time for suffix tree
            # print(f"Searching for '{string}' in Suffix Tree...")
            time_suffix_tree = measure_time(search_tree, suffix_tree, string)
            results['SuffixTree'].append((len(string), time_suffix_tree))
            # print(f"SuffixTree search time for '{string}': {time_suffix_tree}")  # Debug statement

    return results

# Function to plot results
def plot_results(results):
    output_folder = os.path.join(os.path.dirname(__file__), '..', 'plots')
    os.makedirs(output_folder, exist_ok=True)

    string_lengths = set(len(s) for s in test_strings)

    for ds_name, times in results.items():
        plt.figure()
        for length in string_lengths:
            length_times = [time for l, time in times if l == length]
            if length_times:  # Check if there are times for this length
                avg_time = sum(length_times) / len(length_times)
                print(f"Plotting {ds_name} for string length {length}: {length_times} (avg: {avg_time})")  # Debug statement
                plt.plot(length, avg_time, 'o', label=f'String Length {length}')
            else:
                print(f"No data for {ds_name} with string length {length}")  # Debug statement
        plt.xlabel('String Length')
        plt.ylabel('Average Time (s)')
        plt.title(f'Search Time for {ds_name}')
        plt.legend()
        plt.savefig(os.path.join(output_folder, f'{ds_name}_search_times.png'))
        plt.close()

if __name__ == "__main__":
    results = run_experiments()
    # print(results)
    plot_results(results)