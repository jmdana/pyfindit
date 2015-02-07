#!/usr/bin/env python
# encoding: utf-8

import re
import os
import argparse

NO_COMMENT = r"(?!.*\s*[#]\s*)"

CLASS = r"%s(class\s*)({keyword})(\s*\(.*$)" % NO_COMMENT
DEF = r"%s(def\s*)({keyword})(\s*\(.*$)" % NO_COMMENT
INIT = r"%s({keyword})(\s*=.*$)" % NO_COMMENT
USE = r"%s(.*[\s\(\[\.])({keyword})(?!\s*[=\w].*)(.*$)" % NO_COMMENT

COLORS = {
    "red": 31,
    "green": 32,
    }

def highlight(string, color="green"):
    bold = "\033[1m"
    tone = "\033[%dm" % COLORS[color]
    reset = "\033[0m"

    return bold + tone + string + reset

def fmt_match(fname, idx, keyword, match):
    out = "%s :%d\t" % (fname, idx)

    for g in match.groups():
        if g.strip() == keyword:
            out += highlight(g, "green")
        elif g.strip() in ("def", "class"):
            out += highlight(g, "red")
        else:
            out += g

    return out

def search_file(fname, pattern, keyword):
    try:
        f = open(fname, "r")
    except FileNotFoundError:
        return

    pattern_re = re.compile(pattern.format(keyword=keyword))

    for idx, line in enumerate(f, start=1):
        m = re.match(pattern_re, line)
        if m:
            print(fmt_match(fname, idx, keyword, m))

    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("keyword", type=str, nargs=1, help="the keyword to find")
    parser.add_argument("path", type=str, nargs="?", default=".", help="the path")

    args, unknown = parser.parse_known_args()

    for root, dirs, fnames in os.walk(args.path):
        for fname in [x for x in fnames if x.endswith(".py")]:
            full_path = os.path.join(root, fname)
            search_file(full_path, CLASS, args.keyword[0])
            search_file(full_path, DEF, args.keyword[0])
            search_file(full_path, INIT, args.keyword[0])
            search_file(full_path, USE, args.keyword[0])

