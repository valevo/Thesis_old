import pickle
import os
import sys

def get_prop(dict_of_dicts, prop, do_print=True, print_keys=True):
    result = {k: v[prop] for k, v in dict_of_dicts.items()}
    if do_print:
        for k, v in sorted(result.items()):
            if print_keys:
                print(k, ": ", v)
            else:
                print(v)
    return result

if __name__ == '__main__':
    # args = sys.argv
    # prop = args[1]
    # if len(args) > 2:
    #     key_print_arg = eval(args[2])
    # else:
    #     key_print_arg = True

    prop = "number of tokens"


    files = os.listdir()
    files = [f for f in files if f.endswith("Splitter")]

    ds = {}

    for f in files:
        file_parts = f.split("_")
        lang = file_parts[0]
        lvl = file_parts[1][:-8]
        with open(f, "rb") as handle:
            cur_d = pickle.load(handle)
            ds[(lang, lvl)] = cur_d


    vals = get_prop(ds, prop)

    prop2 = "tokens in intersection"

    print()

    vals2 = get_prop(ds, prop2)

    d_diff = {k : v/vals[k] for k, v in vals2.items()}

    print("\n\n" + "."*100)

    for k, v in sorted(d_diff.items()):
        print(k, ':', v)

    for (l, lvl), v in sorted(d_diff.items()):
        if lvl == "Article":
            print(vals2[(l, lvl)], end=" ")
            print("(", round(v, 3), ") &", end=" ")
