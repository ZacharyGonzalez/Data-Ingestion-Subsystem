from readers.csv_reader import get_csv

HEALTHCARE_CSV_PATH = './data/healthcare_dataset.csv'
healthcare_dataframe = get_csv(HEALTHCARE_CSV_PATH)

healthcare_dataframe.drop_duplicates()
healthcare_dataframe.dropna()
healthcare_dataframe['Name']=healthcare_dataframe['Name'].str.title()
healthcare_dataframe['Billing Amount'] = healthcare_dataframe['Billing Amount'].round(2) 
healthcare_dataframe.columns = healthcare_dataframe.columns.str.strip().str.lower().str.replace(' ','_') 