import pandas as pd

def convert_df(df):
    return df.to_csv().encode('utf-8')
