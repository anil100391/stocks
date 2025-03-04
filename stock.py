import genericpath
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
class StockInfo:

    def __init__(self, symbol: str, isincode: str, name: str, sector: str) -> None:
        self.symbol = symbol
        self.isincode = isincode
        self.name = name
        self.sector = sector

    def __repr__(self) -> str:
        return self.name


#################################################################################
#################################################################################
class Stock:

    symbolToStockInfo: dict[str, StockInfo] = {}
    nameToSymbol: dict[FuzzyStr, str] = {}
    isinCodeToSymbol: dict[str, str] = {}

    def __init__(self, symbol: str, symbolInfo=None):
        self.symbol = symbol
        self.info = symbolInfo if symbolInfo else Stock.symbolToStockInfo.get(symbol)

    def __repr__(self) -> str:
        return str(self.info)


#################################################################################
#################################################################################
def PopulateStocks():

    with open("data/EQUITY_L.csv", newline="\n") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            symbol = row.get("SYMBOL")
            companyName = row.get("NAME OF COMPANY")
            isinCode = row.get("ISIN NUMBER")
            sector = "unknown"
            if not symbol or not companyName or not isinCode:
                continue

            if Stock.symbolToStockInfo.get(symbol):
                continue

            Stock.symbolToStockInfo[symbol] = StockInfo(
                symbol, isinCode, companyName, sector
            )
            Stock.nameToSymbol[FuzzyStr(companyName)] = symbol
            Stock.isinCodeToSymbol[isinCode] = symbol


#################################################################################
#################################################################################
SECTOR_FILES = {
    "auto": ["data/ind_niftyautolist.csv"],
    "consumer durables": ["data/ind_niftyconsumerdurableslist.csv"],
    "finance": [
        "data/ind_niftyfinancelist.csv",
        "data/ind_niftyfinancialservices25-50list.csv",
        "data/ind_niftymidsmallfinancailservice_list.csv",
        "data/ind_niftybanklist.csv",
        "data/ind_nifty_privatebanklist.csv",
        "data/ind_niftypsubanklist.csv",
    ],
    "fmcg": ["data/ind_niftyfmcglist.csv"],
    "it": ["data/ind_niftyitlist.csv", "data/ind_niftymidsmallitAndtelecom_list.csv"],
    "healthcare": [
        "data/ind_niftyhealthcarelist.csv",
        "data/ind_niftymidsmallhealthcare_list.csv",
        "data/ind_niftypharmalist.csv",
    ],
    "media": ["data/ind_niftymedialist.csv"],
    "metal": ["data/ind_niftymetallist.csv"],
    "oil and gas": ["data/ind_niftyoilgaslist.csv"],
    "reality": ["data/ind_niftyrealtylist.csv"],
    "services": [],
    "infrastructure": [],
    "chemicals": [],
    "textiles": [],
    "unknown": [],
}

#################################################################################
#################################################################################
SECTORS = [sector for sector in SECTOR_FILES]


#################################################################################
#################################################################################
def PopulateSectorStocks():

    for sector in SECTORS:
        for sectorFile in SECTOR_FILES[sector]:
            PopulateStocksFromSector(sector, sectorFile)


#################################################################################
#################################################################################
def PopulateStocksFromSector(sector: str, sectorFile: str):

    with open(sectorFile, newline="\n") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            symbol = row.get("Symbol")
            companyName = row.get("Company Name")
            isinCode = row.get("ISIN Code")
            if not symbol or not companyName or not isinCode:
                print("Invalid Data: ", symbol, companyName, isinCode)
                continue

            existingStock = Stock.symbolToStockInfo.get(symbol)
            if existingStock:
                continue

            Stock.symbolToStockInfo[symbol] = StockInfo(
                symbol, isinCode, companyName, sector
            )
            Stock.nameToSymbol[FuzzyStr(companyName)] = symbol
            Stock.isinCodeToSymbol[isinCode] = symbol


#################################################################################
#################################################################################
def PopulateNiftyTotalStocks():

    industriesToSector = {
        "Consumer Services": "services",
        "Services": "services",
        "Consumer Durables": "consumer durables",
        "Construction": "infrastructure",
        "Healthcare": "healthcare",
        "Power": "oil and gas",
        "Metals & Mining": "metal",
        "Construction Materials": "infrastructure",
        "Financial Services": "finance",
        "Diversified": "unknown",
        "Telecommunication": "it",
        "Fast Moving Consumer Goods": "fmcg",
        "Capital Goods": "unknown",
        "Forest Materials": "unknown",
        "Automobile and Auto Components": "auto",
        "Utilities": "unknown",
        "Information Technology": "it",
        "Oil Gas & Consumable Fuels": "oil and gas",
        "Chemicals": "chemicals",
        "Realty": "reality",
        "Textiles": "textiles",
        "Media Entertainment & Publication": "media",
    }
    with open("data/ind_niftytotalmarket_list.csv", newline="\n") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            symbol = row.get("Symbol")
            companyName = row.get("Company Name")
            isinCode = row.get("ISIN Code")
            if not symbol or not companyName or not isinCode:
                print("Invalid Data: ", symbol, companyName, isinCode)
                continue

            existingStock = Stock.symbolToStockInfo.get(symbol)
            if existingStock:
                continue

            industry = row.get("Industry")
            sector = industriesToSector.get(industry) if industry else "unknown"
            if not sector:
                sector = "unknown"

            if not sector in SECTORS:
                print("Invalid Sector: ", sector, symbol, companyName, isinCode)
            assert sector in SECTORS
            Stock.symbolToStockInfo[symbol] = StockInfo(
                symbol, isinCode, companyName, sector
            )
            Stock.nameToSymbol[FuzzyStr(companyName)] = symbol
            Stock.isinCodeToSymbol[isinCode] = symbol


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
        stockInfo = Stock.symbolToStockInfo.get(symbol)
        if stockInfo:
            print(stockInfo.name, name, coherence(stockInfo.name, name))

    # if not symbol:
    #     print("NOT FOUND", name)

    return Stock(symbol) if symbol else None


#################################################################################
#################################################################################
def CreateStockFromIsinCode(isinCode: str) -> Stock | None:

    symbol = Stock.isinCodeToSymbol.get(isinCode)
    return Stock(symbol) if symbol else None


PopulateSectorStocks()
PopulateNiftyTotalStocks()
PopulateStocks()
