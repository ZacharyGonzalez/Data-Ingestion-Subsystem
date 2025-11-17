import pandas as pd


# SINGLETON THIS LATER
def standardize_names(df, logger): 
    logger.info(f'Standardizing Names.')
    df['Name']=df['Name'].str.title()
    return df
    
    
def standardize_bill(df,logger):
    logger.info(f'Standardizing Bill Amount.')
    df['Billing Amount'] = df['Billing Amount'].round(2) 
    return df
   
   
def standardize_columns(df,logger):
    logger.info(f'Standardizing the column names.')
    df.columns = df.columns.str.strip().str.lower().str.replace(' ','_')  
    return df


def clean_data(df, logger)->pd.DataFrame:
    df = standardize_names(df,logger)
    df = standardize_bill(df,logger)
    df = standardize_columns(df,logger)
    return df
    