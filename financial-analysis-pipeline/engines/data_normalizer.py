import pandas as pd
def normalize_financial_df(df):
    df = df.copy()
    df['Amount'] = (
        df['Amount']
            .astype(str)
            .str.replace(',', '', regex=False)
            .str.replace('(', '-', regex=False)
            .str.replace(')', '', regex=False)
            .str.strip()
    )
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    return df
