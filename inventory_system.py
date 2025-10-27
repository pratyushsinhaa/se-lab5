import json
import logging
from datetime import datetime

# Global variable
stock_data = {}

def addItem(item="default", qty=0, logs=None):
    # Fix 1: avoid mutable default by using None sentinel
    if logs is None:
        logs = []

    # Fix 2: basic input validation to avoid TypeError at runtime
    if not isinstance(item, str):
        logging.warning("addItem: item must be a string: %r", item)
        return
    try:
        qty_int = int(qty)
    except (TypeError, ValueError):
        logging.warning("addItem: qty must be an integer: %r", qty)
        return

    if not item:
        return
    stock_data[item] = stock_data.get(item, 0) + qty_int
    logs.append("%s: Added %d of %s" % (str(datetime.now()), qty_int, item))

def removeItem(item, qty):
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        # Fix 3: handle the specific error (item missing)
        logging.warning("removeItem: item %r not found", item)
    except TypeError:
        # also handle bad qty type
        logging.warning("removeItem: qty must be a number: %r", qty)

def getQty(item):
    return stock_data[item]

def loadData(file="inventory.json"):
    f = open(file, "r")
    global stock_data
    stock_data = json.loads(f.read())
    f.close()

def saveData(file="inventory.json"):
    f = open(file, "w")
    f.write(json.dumps(stock_data))
    f.close()

def printData():
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])

def checkLowItems(threshold=5):
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def main():
    addItem("apple", 10)
    addItem("banana", -2)
    addItem(123, "ten")  # invalid types, now detected and will be ignored
    removeItem("apple", 3)
    removeItem("orange", 1)
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()
    # Fix 4: removed eval usage for security reasons
    logging.info("eval removed for security reasons")

# Fix 5: guard to prevent execution during import/static analysis
if __name__ == "__main__":
    main()