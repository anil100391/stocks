import pymupdf
from stock import *

#################################################################################
#################################################################################
mystocks = []
doc = pymupdf.open("Demat_Report_0685137538_27-02-2025.pdf")
for page in doc:
    text = page.get_text()
    lines = text.split("\n")
    for line in lines:
        if line.isupper():
            stock = CreateStockFromName(line)
            if stock:
                mystocks.append(stock)

print("My Stocks: ", len(mystocks))
for i in range(len(mystocks)):
    print(i, ": ", mystocks[i])
