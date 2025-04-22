# inventory
"""
three types of items:
- stackables (wheat)
- multi-tier tools (wood axe, copper hoe)
- non-stackables (ex: filled/empty buckets, fishing rod)
"""
theInventory = [
    [None, ("Banana", 6), None, None],
    [None, None, None, ("Milk", 1)],
    [None, ("Water", 34), None, ("Butter", 14)],
    [("Tea Leaves", 6), None, None, ("Wheat", 34)],
]

def baseItemString(item) -> str:
    if isinstance(item, tuple): return item[0]
    elif isinstance(item, str): return item
    else: return "Empty"

def itemStateString(item) -> str:
    # return item tier/bucket state if the item is non-stackable
    # else return quantity if item is stackable
    # else return unknown
    if isinstance(item, tuple):
        secondPart = item[1]
        if (isinstance(secondPart, int)): return "x" + str(secondPart)
        else: return "Unknown"
    else: return "Empty"

def parseInventoryItem(item) -> str:
    if isinstance(item, tuple): return itemStateString(item) + " " + baseItemString(item)
    elif isinstance(item, str): return item
    else: return "None"

def parseStacklessInventoryItem(item) -> str:
    if isinstance(item, tuple):
        if isinstance(item[1], int): return baseItemString(item)
    return parseInventoryItem(item)

def isTupleOrString(item) -> bool:
    if (not isinstance(item, tuple) and not isinstance(item, str)):
        print(f"the item {item} was not a tuple or a string!")
        return False
    return True

def isValidTuple(item) -> bool:
    if (not isinstance(item[1], int)): return False
    return True

def isInvalidName(item) -> bool:
    if (len(str(item)) < 1):
        print(f"the item you tried inserting was a string, but its name is empty!")
        return False
    return True

def putInSlot(item, row: int, column: int):
    if item is not None:
        if not isTupleOrString(item): return None
        elif isinstance(item, tuple) and not isValidTuple(item): return None
        elif isinstance(item, str) and not isInvalidName(item): return None
        elif not theInventory[row][column] == None:
            print(f"the inventory at row {row} and column {column} is not empty!")
            return None
    theInventory[row][column] = item
    print(f"item {item} was placed in row {row} and column {column} of the inventory")

def hasEnoughOfItem(item) -> bool:
    if item is None: return False
    for row in range(len(theInventory)):
        for column in range(len(theInventory[row])):
            itemAt = theInventory[row][column]
            if itemAt is None: continue
            elif not isinstance(itemAt, tuple): continue
            elif not isinstance(itemAt[0], str): continue
            elif itemAt[0] != item[0]: continue
            elif isinstance(itemAt[1], int) and isinstance(item[1], int):
                if item[1] > itemAt[1]: return False
                else: return True
    return False

def quantityForItem(item) -> int:
    if item is None or not hasEnoughOfItem(item): return 0
    for row in range(len(theInventory)):
        for column in range(len(theInventory[row])):
            itemAt = theInventory[row][column]
            if itemAt is None: continue
            elif isinstance(itemAt, str) and isinstance(item, str) and itemAt == item: return 1
            elif isinstance(itemAt, tuple) and isinstance(item, tuple) and itemAt[0] == item[0]:
                if isinstance(item[1], int) and isinstance(itemAt[1], int): return itemAt[1]
                else: return 1
    return 0

def insertItemIntoSpareSlot(item):
    for row in range(len(theInventory)):
        for column in range(len(theInventory[row])):
            itemAt = theInventory[row][column]
            if itemAt is not None:
                if isinstance(item, tuple) and item[0] == itemAt[0] and isinstance(itemAt[1], int) and isinstance(item[1], int):
                    updatedQuantity = itemAt[1] + item[1]
                    putInSlot(None, row, column)
                    if (updatedQuantity > 0): putInSlot((item[0], updatedQuantity), row, column)
                    return
                else: continue
            elif quantityForItem(item) == 0:
                putInSlot(item, row, column)
                return