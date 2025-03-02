import genericpath
from stock import *
import csv


#################################################################################
#################################################################################
class FuzzyStr:

    def __init__(self, string: str) -> None:
        self.string = string.lower()

    def __eq__(self, other) -> bool:
        return self.string == other.string

    def __hash__(self) -> int:
        return self.string.__hash__()

    def __repr__(self) -> str:
        return self.string


#################################################################################
#################################################################################
def coherence(left: str, right: str) -> float:

    if left == right:
        return 20

    lhs = left.lower().split()
    rhs = right.lower().split()

    if "ltd" in lhs:
        lhs[lhs.index("ltd")] = "limited"

    if "ltd" in rhs:
        rhs[rhs.index("ltd")] = "limited"

    genericKeyword = ["limited", "(i)", "india", "industries", "green", "energy"]
    score = 0
    for i in lhs:
        wt = 0.01 if i in genericKeyword else 1.0
        if i in rhs:
            score += wt

    return score


#################################################################################
#################################################################################
class Stock:

    symbolToName: dict[str, str] = {}
    nameToSymbol: dict[FuzzyStr, str] = {}

    def __init__(self, symbol: str, name=None) -> None:
        self.symbol = symbol
        self.name = name if name else self.symbolToName.get(self.symbol)

    def __repr__(self) -> str:
        if not self.name:
            raise RuntimeWarning("unknown name")
        return self.name


#################################################################################
#################################################################################
def PopulateStocks():

    with open("EQUITY_L.csv", newline="\n") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            symbol = row.get("SYMBOL")
            companyName = row.get("NAME OF COMPANY")
            if not symbol or not companyName:
                continue

            Stock.symbolToName[symbol] = companyName
            Stock.nameToSymbol[FuzzyStr(companyName)] = symbol


#################################################################################
#################################################################################
def CreateStockFromName(name: str) -> Stock | None:

    symbol = Stock.nameToSymbol.get(FuzzyStr(name))

    notFound = symbol is None
    if not symbol:
        maxScore = 0
        for stockName in Stock.nameToSymbol:
            score = max(coherence(str(stockName), name), maxScore)
            if score > maxScore:
                maxScore = score
                if score > 1:
                    symbol = Stock.nameToSymbol[stockName]

    if symbol and notFound:
        sname = Stock.symbolToName.get(symbol)
        if sname:
            print(sname, name, coherence(sname, name))

    if not symbol:
        print("NOT FOUND", name)

    return Stock(symbol) if symbol else None


PopulateStocks()
