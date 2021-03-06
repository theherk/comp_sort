"""
Sort composite dictionary based on predifined rules.

text
dicts
lists

sort_order list - ['rn', 'port']
"""
import json
from collections import OrderedDict


def dict_sort(item, order=None):
    """
    Function as key to sort data models to order:
    string/int/(other), dict, list

    0 + string # priority strings
    1 + string # strings
    2 + string # priority dicts
    3 + string # dicts
    4 + string # priority lists
    5 + string + lists
    """
    def seq(s, o=None, v=None):
        return str(s) + str(o) + str(v) if o is not None else str(s)

    order_seq = None
    if order is not None and item[0] in order:
        order_seq = [i for i, v in enumerate(order) if v == item[0]][0]

    if isinstance(item[1], dict):
        return seq(2, order_seq, item[0]) if order_seq else seq(3)
    elif isinstance(item[1], list):
        return seq(4, order_seq, item[0]) if order_seq else seq(5)
    else:
        return seq(0, order_seq, item[0]) if order_seq else seq(1)


def comp_sort(data, order=None):
    """
    Sort a composite dictionary made up of strings, dicts, or lists.
    (unserialized json object)
    """
    odata = OrderedDict()
    if isinstance(data, dict):
        for k, v in sorted(data.items(), key=lambda d: dict_sort(d, order)):
            if isinstance(v, dict) or isinstance(v, list):
                odata[k] = comp_sort(v, order)
            else:
                odata[k] = v
    elif isinstance(data, list):
        try:
            return sorted(data)
        except:
            items = []
            for v in data:
                if isinstance(v, dict) or isinstance(v, list):
                    items.append(comp_sort(v, order))
                else:
                    items.append(v)
            return items
    return odata


with open('derp.json') as f:
    data = json.load(f)

sort_order = ['rn', 'port']
odata = comp_sort(data, sort_order)

from pprint import pprint
pprint(odata)
