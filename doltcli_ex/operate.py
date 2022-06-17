#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from typing import Dict, List, Tuple, Union

import pandas as pd
from doltcli import Dolt, write_rows

from doltcli_ex.io import read_json

CONVENTION_FILES = ["README.md", "LICENSE.md"]
DATA_MODE_NAMES = ["train", "dev", "test", "submit", "trial"]


def transform(filepath: Union[str, Path]) -> Tuple[str, List[Dict]]:
    """transform data file into a list of dict (rows)

    Args:
        filepath (Union[str, Path]): data file path

    Raises:
        Exception: raise when some wrong data format or content occurs.

    Returns:
        Tuple[str, List[Dict]]: name and the rows
    """

    basename = os.path.basename(filepath)
    name, suffix = basename.split(".")

    if suffix == "csv":
        return name, pd.read_csv(filepath).to_dict(orient="records")

    elif suffix == "json":
        data = read_json(filepath)
        if data is not None:
            return name, list(data)

        else:
            raise Exception("None of data")

    else:
        raise Exception("Invalid Format")


def add(path: Union[str, Path]) -> None:
    """ehanced add method

    Args:
        path (Union[str, Path]): a specific data/md file path or a table name
    """
    assert not os.path.isdir(path), "Cannot add a folder! Please add a single data file"
    basename = os.path.basename(path)

    cwd = os.getcwd()
    repo = Dolt(cwd)

    if basename.endswith(".json") or basename.endswith(".csv"):
        name, rows = transform(path)
        write_rows(repo, name, rows, primary_key=["_id"], do_continue=True)
        repo.add(name)

    elif basename in CONVENTION_FILES + DATA_MODE_NAMES:
        repo.add(basename)

    else:
        # TODO: more friendly solution
        repo.add(basename)


def remove(name: str) -> None:
    """enhance remove method

    Args:
        name (str): name of a specific md file or table
    """
    cwd = os.getcwd()
    repo = Dolt(cwd)

    if name in CONVENTION_FILES:
        os.remove(name)

    elif name in DATA_MODE_NAMES:
        repo.execute(args=["table", "rm", name])

    else:
        # TODO: more friendly solution
        repo.execute(args=["table", "rm", name])
