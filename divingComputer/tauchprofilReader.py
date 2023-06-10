import csv

with open('DivingComputer\divingprofile.txt', 'r') as fin:
    for line in csv.DictReader(fin, delimiter='\t'):
        print(line)

