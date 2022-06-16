#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

import pandas as pd


def _read_json_per_line(
    file_path: Union[str, Path], filter_: Optional[Callable], ignore_exception
):
    with open(file_path) as f:
        for line in f:
            try:
                data = json.loads(line)
                if filter_ is None or filter_(data):
                    yield data
            except Exception as e:
                if not ignore_exception:
                    raise e


def read_json(
    file_path: Union[str, Path],
    per_line_mode: bool = True,
    filter_: Optional[Callable] = None,
    ignore_exception: bool = False,
) -> Union[Iterable[Dict], Dict]:
    """helper to read json file

    Args:
        file_path (Union[str,Path]): json file path

        per_line_mode (bool, optional): whether the json data is list-like or dict-like.
            Defaults to True.If True,it will read the data one line by one line and return a list-like object.
            Otherwise it will return a dict-like object.

        filter_ (Optional[Callable], optional): a data filter function with a bool return.
            Defaults to None.If not None,only return the data with True value in filter function.

        ignore_exception (bool, optional): whether ignore exceptions raised when reading the data.
            Defaults to False.

    Raises:
        e: raise exception when some inner error of data occurs, and ignore_exception param is False

    Returns:
        Union[Iterable[Dict], Dict]: result
    """

    if per_line_mode:
        return _read_json_per_line(file_path, filter_, ignore_exception)
    else:
        data = None
        with open(file_path) as f:
            try:
                data = json.load(f)
            except Exception as e:
                if not ignore_exception:
                    raise e
            return data


def dump_json(
    objs: Union[Iterable[Any], Any],
    file_path: str,
    per_line_mode: bool = True,
    ensure_ascii: bool = False,
) -> None:
    """dump json file

    Args:
        objs (Union[Iterable[Any], Any]): objects to be dumped

        file_path (str): json file path

        per_line_mode (bool, optional): whether the json data is list-like or dict-like.
            Defaults to True.If True,it will read the data one line by one line and return a list-like object.
            Otherwise it will return a dict-like object.

        ensure_ascii (bool, optional): ensure_ascii.
            Defaults to False.
    """
    with open(file_path, "w") as f:
        if per_line_mode:
            for obj in objs:
                json.dump(obj, f, ensure_ascii=ensure_ascii)
                f.write("\n")
        else:
            json.dump(objs, f, ensure_ascii=ensure_ascii)


def check_files_exist(
    data_dir: str, name: str, ignore_exception: bool = False
) -> List[str]:
    """check whether some files with specific pattern exist or not

    Args:
        data_dir (str): which data directory to be watched out

        name (str): name pattern to be matched

        ignore_exception (bool, optional): whether ignore exception or not.
            Defaults to False.

    Raises:
        Exception: raise when no matched files

    Returns:
        List[str]: paths of all matched files
    """
    names = os.listdir(data_dir)
    names = [n for n in names if n.split(".")[0] == name]
    files_paths = [os.path.join(data_dir, name) for name in names]
    if len(files_paths) == 0:
        if not ignore_exception:
            raise Exception(f"No file named {name} in {data_dir}")

    return files_paths
