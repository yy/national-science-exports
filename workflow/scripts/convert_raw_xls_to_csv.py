""" This script converts a raw Excel file into a csv file.

argv[1]: The raw excel file (full counting, fractional counting, and
         corresponding)

argv[2]: The converted CSV file

"""

import sys

import pandas as pd

# The data is in the Sheet1 in all raw data files.
SHEET_NAME = "Sheet1"
COUNTRY_PUB_RECORD_RAW_FILE = sys.argv[1]
CSV_FILE = sys.argv[2]

pd.read_excel(
    COUNTRY_PUB_RECORD_RAW_FILE,
    sheet_name=SHEET_NAME,
    names=["YEAR", "DISCIPLINE", "SPECIALTY", "COUNTRY", "PAPER_CNT"],
    engine="openpyxl",
).to_csv(CSV_FILE, index=False)
