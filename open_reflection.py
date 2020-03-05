path = './reflection_from_well.txt'

with open(path) as f:
    for line in f:
        # no idea how to split on \n
        cleaned_line = line.strip().split('\\n')
        print(cleaned_line)
