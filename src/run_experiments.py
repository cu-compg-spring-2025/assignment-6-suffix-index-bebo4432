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
data_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.fa.gz')]

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
        if 'wuhana-hu' in data_file or 'chr22' in data_file:
            continue

        with gzip.open(data_file, 'rt') as file:
            file.readline()  # Skip the first line
            while True:
                data = file.read(1000)  # Read the next 1000 bases
                if not data:
                    break

                # Build data structures
                suffix_array = build_suffix_array(data)
                suffix_trie = build_suffix_trie(data)
                suffix_tree = build_suffix_tree(data)

                for string in test_strings:
                    # Measure search time for suffix array
                    time_suffix_array = measure_time(search_array, data, suffix_array, string)
                    results['SuffixArray'].append((len(string), time_suffix_array))

                    # Measure search time for suffix trie
                    time_suffix_trie = measure_time(search_trie, suffix_trie, string)
                    results['SuffixTrie'].append((len(string), time_suffix_trie))

                    # Measure search time for suffix tree
                    time_suffix_tree = measure_time(search_tree, suffix_tree, string)
                    results['SuffixTree'].append((len(string), time_suffix_tree))

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
                plt.hist(length_times, bins=30, alpha=0.5, label=f'String Length {length}')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency')
        plt.title(f'Distribution of Search Times for {ds_name}')
        plt.legend()
        plt.savefig(os.path.join(output_folder, f'{ds_name}_search_times_distribution.png'))
        plt.close()

if __name__ == "__main__":
    results = run_experiments()
    plot_results(results)