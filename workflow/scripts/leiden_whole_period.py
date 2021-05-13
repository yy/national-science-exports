import pandas as pd
import sys

LEIDEN_PERIOD=sys.argv[1]
OUTPUT=sys.argv[2]

period_df=pd.read_csv(LEIDEN_PERIOD,sep=",")


period_df[period_df.whole!=period_df.group].to_csv(OUTPUT,sep=",")
