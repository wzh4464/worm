import pandas as pd

csv_file = 'work_on_csv.csv'

# I want to split each line of it. I want to put the last two part in the first place and leave others to the third place. In the third place, if there is a comma, I want to change the comma to '*'.

with open(csv_file, 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        line_parts = line.split(',')
        new_line = ''
        new_line += line_parts[-2] + ',' + line_parts[-1] + ','
        the_third_part = []
        # joint the remaind with '*' and put them in the third place
        for part in line_parts[:-2]:
            the_third_part.append(part)
        the_third_part = '*'.join(the_third_part)
        print(new_line)
        with open('new_result.csv', 'a+') as f:
            f.write(new_line + the_third_part + '\n')