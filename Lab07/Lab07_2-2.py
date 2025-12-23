import os

def find_longest_word_in_lines(input_file, output_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, input_file)
    output_path = os.path.join(script_dir, output_file)
    
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        for line_num, line in enumerate(infile, 1):
            words = line.strip().split()
            if words:
                longest_word = max(words, key=len)
                outfile.write(f"{longest_word}\n")
            else:
                outfile.write("\n")

find_longest_word_in_lines("input.txt", "output.txt")
print("Результат записан в output.txt в той же папке, где находится программа.")