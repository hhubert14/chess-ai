import csv

# Adjustable variable
file_path = 'C:/Users/huang/repos/Personal/chess-ai/datasets/train_puzzles.csv'

with open(file_path, 'r') as file:
    reader = csv.reader(file)
    row_count = sum(1 for row in reader)

print(f'The number of rows in the file is: {row_count}')
