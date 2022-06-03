#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import uuid

import pandas as pd
import requests
from loguru import logger


def paginate_format(pagination):
    pagination.__dict__["pages"] = int(pagination.total / pagination.per_page) + (
        1 if pagination.total % pagination.per_page > 0 else 0
    )
    pagination.__dict__["has_previous"] = True if pagination.page > 1 else False
    pagination.__dict__["has_next"] = (
        True if pagination.page < pagination.pages else False
    )
    pagination.__dict__["next_page"] = (
        pagination.page + 1 if pagination.has_next is True else None
    )
    pagination.__dict__["previous_page"] = (
        pagination.page - 1 if pagination.has_previous is True else None
    )
    return pagination


def remove_none_in_dict(data: dict) -> dict:
    return {key: value for key, value in data.items() if value is not None}


def remove_file(path):
    if os.path.isfile(path):
        os.remove(path)


def download_file(file_url):
    r = requests.get(file_url)
    path = f"{uuid.uuid1()}.xls"
    open(path, "wb").write(r.content)
    return path


def make_df_from_excel(file_path, nrows):
    """Read from an Excel file in chunks and make a single DataFrame.

    Parameters
    ----------
    file_name : str
    nrows : int
        Number of rows to read at a time. These Excel files are too big,
        so we can't read all rows in one go.
    """
    xl = pd.ExcelFile(file_path)

    # In this case, there was only a single Worksheet in the Workbook.
    sheetname = xl.sheet_names[0]

    # Read the header outside of the loop, so all chunk reads are
    # consistent across all loop iterations.
    df_header = pd.read_excel(file_path, sheet_name=sheetname, nrows=0, dtype=str)
    logger.info(f"Excel file: {file_path} (worksheet: {sheetname})")

    chunks = []
    i_chunk = 0
    # The first row is the header. We have already read it, so we skip it.
    skiprows = 1
    while True:
        df_chunk = pd.read_excel(
            file_path,
            sheet_name=sheetname,
            nrows=nrows,
            skiprows=skiprows,
            header=None,
            dtype=str,
        )
        skiprows += nrows
        # When there is no data, we know we can break out of the loop.
        if not df_chunk.shape[0]:
            break
        else:
            print(f"  - chunk {i_chunk} ({df_chunk.shape[0]} rows)")
            chunks.append(df_chunk)
        i_chunk += 1

    if len(chunks) == 0:
        df = pd.concat([df_header])
    else:
        df_chunks = pd.concat(chunks)
        # Rename the columns to concatenate the chunks with the header.
        columns = {i: col for i, col in enumerate(df_header.columns.tolist())}
        df_chunks.rename(columns=columns, inplace=True)
        df = pd.concat([df_header, df_chunks])
    return df
