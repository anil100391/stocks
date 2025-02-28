import csv

symbols = []

with open('MW-NIFTY-200-27-Feb-2025.csv', encoding='utf-8-sig', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        symbols.append(row['SYMBOL '])

symbols = list(set(symbols))
print(len(symbols))
print(symbols)
