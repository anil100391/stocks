import pymupdf

mystocks = []
doc = pymupdf.open("Demat_Report_0685137538_27-02-2025.pdf")
for page in doc:
    text = page.get_text()
    lines = text.split("\n")
    for line in lines:
        if line.isupper():
            mystocks.append(line.strip().lower())

mystocks = list(set(mystocks))

nse = {}
with open("nse1.txt") as f:
    lines = f.readlines()
    for line in lines:
        k, v = line.split('\t')
        v.strip()
        nse[v.lower().strip()] = k

print("NSE Stocks: ", len(nse))
#print(nse)
print("My Stocks: ", len(mystocks))
#print(mystocks)

found = 0
not_found = 0
for stock in mystocks:
    if stock.lower() in nse:
        print(stock, ": ", nse[stock.lower()])
        found += 1
    else:
        #print(stock, ": NOT FOUND")
        not_found += 1

print("Found: ", found)
print("Not Found: ", not_found)
#
#
#

