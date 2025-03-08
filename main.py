from stock import *
from readpdf import *
import sys


#################################################################################
#################################################################################
def analyze(pdf_file: str, pdf_credentials: str | None = None):
    mystocks = []

    if not pdf_file:
        raise RuntimeError("PDF file not specified")

    text = read_pdf(pdf_file, pdf_credentials)

    lines = text.split("\n")
    switch0 = False
    switch1 = False

    stockInfo = False
    stockInfoLine = 0

    stock = None
    stockQty = 0
    stockRate = 0

    for line in lines:

        if line == "HOLDINGS BALANCE":
            switch0 = True

        if not switch0:
            continue

        if line == "Value":
            switch1 = True
            continue

        if not switch1:
            continue

        if line == "ISIN Code":
            switch1 = False
            continue

        if line == "Total":
            break

        if line.isdigit():
            continue

        if not stockInfo:
            stockInfo = line.isupper()

        if stockInfo:
            if stockInfoLine == 0:
                stock = CreateStockFromIsinCode(line)
                # if not stock:
                #     print("Stock not found for ISIN Code: ", line)
            elif stockInfoLine == 1 and not stock:
                stock = CreateStockFromName(line)
                # if not stock:
                #     print("Stock not found for Name: ", line)
            elif stockInfoLine == 2:
                stockQty = float(line)
            elif stockInfoLine == 10:
                stockRate = float(line)

            stockInfoLine += 1
            if stockInfoLine == 11:
                if stock:
                    mystocks.append((stock, stockQty, stockRate))

                stock = None
                stockQty = 0
                stockRate = 0
                stockInfo = False
                stockInfoLine = 0

    print(
        "---------------------------------------------------------------------------------"
    )
    print("Index\tName\t\t\t\t\t\tQty\tRate")
    print(
        "---------------------------------------------------------------------------------"
    )
    for i in range(len(mystocks)):
        print(
            "{0: <2}".format(i),
            ": ",
            "{0: <50}".format(str(mystocks[i][0])),
            "{0: <5}".format(int(mystocks[i][1])),
            mystocks[i][2],
        )

    sectorWiseCash: dict[str, float] = {}
    marketCapWiseCash: dict[str, float] = {}

    def mcap(marketCap):
        if marketCap == 0:
            return "unknown"

        if marketCap < 5000:
            return "smallcap"

        if marketCap >= 5000 and marketCap < 20000:
            return "midcap"

        return "largecap"

    for i in range(len(mystocks)):
        stock = mystocks[i][0]
        qty = mystocks[i][1]
        rate = mystocks[i][2]
        sector = stock.info.sector
        if sector not in sectorWiseCash:
            sectorWiseCash[sector] = 0
        sectorWiseCash[sector] += qty * rate

        cap = mcap(stock.info.marketcap)
        if cap not in marketCapWiseCash:
            marketCapWiseCash[cap] = 0
        marketCapWiseCash[cap] += qty * rate

    print(
        "---------------------------------------------------------------------------------"
    )

    print("Sector\t\t\tCash")
    print(
        "---------------------------------------------------------------------------------"
    )
    for k in sectorWiseCash:
        print("{0: <20}".format(k), ": ", sectorWiseCash[k])

    print(
        "---------------------------------------------------------------------------------"
    )

    print("MarketCap\t\tCash")
    print(
        "---------------------------------------------------------------------------------"
    )
    for k in marketCapWiseCash:
        print("{0: <20}".format(k), ": ", marketCapWiseCash[k])

    print(
        "---------------------------------------------------------------------------------"
    )

    import matplotlib.pyplot as plt

    values = []
    labels = []
    for k in marketCapWiseCash:
        values.append(marketCapWiseCash[k])
        labels.append(k)
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.show()


if __name__ == "__main__":
    try:
        _, function, *args = sys.argv
        function = globals()[function]
    except:
        print(
            "Usage: python main.py analyze [TRANSACTION_HOLDINGS_STATEMENT_PDF] [PAN]"
        )
    else:
        function(*args)
