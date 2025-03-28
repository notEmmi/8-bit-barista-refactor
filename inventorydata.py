from enum import Enum

class ToolsTiers(Enum):
    Wood = 0,
    Stone = 1,
    Copper = 2,
    Iron = 3

class BucketStates(Enum):
    Empty = 0,
    Filled = 1,

# inventory
"""
three types of items:
- stackables (wheat)
- multi-tier tools (wood axe, copper hoe)
- non-stackables (ex: filled/empty buckets, fishing rod)
"""
theInventory = [
    [("Axe", ToolsTiers.Wood), "Fishing Rod", None, None],
    [None, ("Hoe", ToolsTiers.Copper), None, ("Milk Bucket", BucketStates.Filled)],
    [None, "Mallet", "Watering Can", None],
    ["Seed Pouch", None, None, ("Wheat", 34)],
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
        if (isinstance(secondPart, ToolsTiers)): return ToolsTiers(secondPart).name
        elif (isinstance(secondPart, BucketStates)): return BucketStates(secondPart).name
        elif (isinstance(secondPart, int)): return "x" + str(secondPart)
        else: return "Unknown"
    else: return "Empty"

def parseInventoryItem(item) -> str:
    if isinstance(item, tuple): return itemStateString(item) + " " + baseItemString(item)
    elif isinstance(item, str): return item
    else: return "None"

def getExtraItemData(item: tuple):
    if (isinstance(item[1], Enum)): return Enum(item[1]).name
    else: return "Unknown"

def isTupleOrString(item) -> bool:
    if (not isinstance(item, tuple) and not isinstance(item, str)):
        print(f"the item {item} was not a tuple or a string!")
        return False
    return True

def isValidTuple(item) -> bool:
    if (not isinstance(item[1], ToolsTiers) and not isinstance(item[1], BucketStates) and not isinstance(item[1], int)):
        print(f"{item} is an enum, but it does not contain information from both ToolsTiers and BucketStates enums *AND* is not stackable")
        return False
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