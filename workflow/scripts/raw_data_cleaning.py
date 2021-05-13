""" This script cleans the raw data and saves into a csv file.

input: the raw file comes from Web of Sicnece (by Vincent Lariviere).

- argv[1]: the raw csv file (e.g. `raw_full.csv`)
- argv[2]: the file that consolidates the changes in the countries, such as
            USSR->Russia).

output (argv[3]): a consolidated csv file.

"""
import pandas as pd
import sys


COUNTRY_PUB_RECORD_FILE = sys.argv[1]
COUNTRY_CONSOLIDATION_FILE = sys.argv[2]
OUTFILE = sys.argv[3]

df = pd.read_csv(COUNTRY_PUB_RECORD_FILE)

# we are simply replacing country names in "ORIGINAL" column with the one in
# the "CHANGED" column.
replacement_dict = (
    pd.read_csv(COUNTRY_CONSOLIDATION_FILE).set_index("ORIGINAL")["CHANGED"].to_dict()
)
df["COUNTRY"].replace(replacement_dict, inplace=True)

# group by year, country, and discipline and then sum the pub count.
df = df.groupby(["YEAR", "DISCIPLINE", "SPECIALTY", "COUNTRY"]).sum().reset_index()
df = df[df.DISCIPLINE!="Unknown"]
df.to_csv(
    OUTFILE, index=False
)
