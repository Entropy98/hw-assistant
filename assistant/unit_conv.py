flunits = {
        'cup'   : 8,
        'oz'    : 1,
        'gallon': 128,
        'quart' : 32,
        'pint'  : 16,
        'tbsp'  : .5,
        'tsp'   : 1/6,
        'liter' : 33.814,
        'ml'    : 1/29.574,
        ''      : 1,
}

munits = {
        'lb'    : 16,
        'oz'    : 1,
        'kg'    : 35.274,
        'g'     : 1/28.35,
        ''      : 1,
}

def convert(val,inunit,outunit):
    if(inunit in flunits and outunit in flunits):
        val = val*flunits[inunit]
        return val/flunits[outunit]
    if(inunit in munits and outunit in munits):
        val = val*munits[inunit]
        return val/munits[outunit]
    return val
