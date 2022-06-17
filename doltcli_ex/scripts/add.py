#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

from doltcli_ex.operate import add


def main():
    path = Path(sys.argv[1]).expanduser().absolute()
    add(path)


if __name__ == "__main__":
    main()
