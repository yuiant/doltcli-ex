#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from doltcli_ex.operate import remove


def main():
    path = sys.argv[1]
    remove(path)


if __name__ == "__main__":
    main()
