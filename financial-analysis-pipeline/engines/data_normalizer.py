import pandas as pd 
def normalize_financial_df(df):
    df = df.copy()# Clean raw formatting
    df['Amount'] = (
        df['Amount']
            .astype(str)
            .str.replace(',','', regex=False)
            .str.replace('(','-', regex=False)
            .str.replace(')','', regex=False)
            .str.strip()
    )

    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')# Enforce deterministic sign logic
    expense_categories = ['COGS','Operating Expenses','Finance Costs']

    df.loc[df['FS Category'].isin(expense_categories),'Amount'] = df.loc[
        df['FS Category'].isin(expense_categories),'Amount'
    ].abs()# Revenue must always be positive
    df.loc[df['FS Category'] =='Revenue','Amount'] = df.loc[
        df['FS Category'] =='Revenue','Amount'
    ].abs()# Tax logic (credit vs expense)
    df.loc[(df['FS Category'] =='Tax') & (df['Amount'] >0),'TaxType'] ='Expense'
    df.loc[(df['FS Category'] =='Tax') & (df['Amount'] <0),'TaxType'] ='Credit'
    return df