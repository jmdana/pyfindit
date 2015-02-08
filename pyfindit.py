#!/usr/bin/env python
# encoding: utf-8

import re
import os
import argparse

NO_COMMENT = r"(?!.*\s*[#]\s*)"

CLASS = r"%s(class)(\s*)({keyword})(\s*\(.*$)" % NO_COMMENT
DEF = r"%s(def)(\s*)({keyword})(\s*\(.*$)" % NO_COMMENT
ASSIGN = r"%s(\s*)({keyword})(\s*)(=)(.*$)" % NO_COMMENT
OTHER = r"%s(?!class)(?!def)(.*[\s\(\[\.,])({keyword})(?!\s*[=\w].*)(.*$)" % NO_COMMENT

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
        if g == keyword:
            out += highlight(g, "green")
        elif g in ("def", "class", "="):
            out += highlight(g, "red")
        else:
            out += g

    return out

def search_pattern(fname, patterns, keyword):
    try:
        f = open(fname, "r")
    except FileNotFoundError:
        return

    for idx, line in enumerate(f, start=1):
        for pattern in patterns:
            m = re.match(pattern, line)
            if m:
                print(fmt_match(fname, idx, keyword, m))
                break

    f.close()

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

    parser.add_argument(
        "-c",
        "--class",
        dest="c",
        action="store_true",
        help="search for class names only")

    parser.add_argument(
        "-d",
        "--def",
        dest="d",
        action="store_true",
        help="search for function names only")

    parser.add_argument(
        "-v",
        "--variable",
        dest="v",
        action="store_true",
        help="search for variable assignments only")

    parser.add_argument(
        "-o",
        "--other",
        dest="o",
        action="store_true",
        help="search for other apperances only")

    parser.add_argument(
        "-i",
        "--ignorecase",
        action="store_true",
        help="ignore case")

    parser.add_argument(
        "keyword",
        type=str,
        nargs=1,
        help="the keyword to find")

    parser.add_argument(
        "path",
        type=str,
        nargs="?",
        default=".",
        help="the path")

    args, _ = parser.parse_known_args()

    patterns = []
    flags = 0

    if not (args.c or args.d or args.v or args.o):
        args.c = True
        args.d = True
        args.v = True
        args.o = True

    if args.c:
        patterns.append(CLASS)
    if args.d:
        patterns.append(DEF)
    if args.v:
        patterns.append(ASSIGN)
    if args.o:
        patterns.append(OTHER)

    if args.ignorecase:
        flags |= re.IGNORECASE

    compiled = []

    for pattern in patterns:
        compiled.append(
            re.compile(pattern.format(keyword=args.keyword[0]), flags)
            )

    for root, _, fnames in os.walk(args.path):
        for fname in [x for x in fnames if x.endswith(".py")]:
            full_path = os.path.join(root, fname)
            search_pattern(full_path, compiled, args.keyword[0])

if __name__ == '__main__':
    main()

