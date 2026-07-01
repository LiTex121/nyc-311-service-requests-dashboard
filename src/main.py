
import pandas as pd
from pathlib import Path

# for fixing Path or Directory not found issues.
Project_Root = Path(__file__).resolve().parent.parent

DataFolder = Project_Root / 'data'

File = DataFolder / 'raw' / '311_Service_Requests_from_2020_to_Present_20260611.csv'

Output_FileName = 'New_Data.csv' # must be .csv
Output = DataFolder / 'Clean' / Output_FileName

def Clean_311_Data(File, Output_Location):

    # this will make folders if missing
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    Path("data/Clean").mkdir(parents=True, exist_ok=True)


    df = pd.read_csv(File)

    Rows, Cols = df.shape

    print(f"Starting Data Cleaning so far this dataset has:\nTotal Cols: {Cols}\nTotal Rows: {Rows}")

    df.columns = df.columns.str.strip().str.lower().str.replace(' ','_')
    print('Changed columns headers to lower case and removed/replaced spaces.')


    Columns_To_Keep = [
        'unique_key',
        'created_date',
        'closed_date',
        'agency',
        'agency_name',
        'borough',
        'problem_(formerly_complaint_type)',
        'status']


 # New dataframe which we will convert into csv.
    df_clean = df[Columns_To_Keep].copy()

    df_clean = df_clean.rename(columns={
        'unique_key' : 'request_id',
        'problem_(formerly_complaint_type)' : 'complaint_type'

        })

    df_clean = df_clean.dropna(subset=[
        "request_id",
        "created_date",
        "agency",
        "agency_name",
        "borough",
        "complaint_type",
        'status'
    ]) 

    df_clean = df_clean.drop_duplicates()
    print("Removed Dups and N/A's")

#                      Date     |  Time
# # formating dates to XXXX-XX-XX | XX:XX:XX 
    df_clean["created_date"] = pd.to_datetime(df_clean["created_date"], format='mixed', dayfirst=True, errors="coerce")
    df_clean["closed_date"] = pd.to_datetime(df_clean["closed_date"], format='mixed', dayfirst=True, errors="coerce")



# Adding a few important missing data for our dashboard.

# Between date created and closed date | can be used to get avg
    df_clean['created_date_to_closed_date'] = (df_clean['closed_date'] - df_clean['created_date']).dt.days

# Month Name and number
    df_clean["created_month_name"] = df_clean["created_date"].dt.month_name()

    df_clean["created_month_number"] = df_clean["created_date"].dt.month



# Outputing new csv file and printing to console
    df_clean.to_csv(Output_Location, index=False)

    print(f"New csv was creadted in {Output_Location} folder.")
    print(f"Total new cols and rows:\nRows: {df_clean.shape[0]} Cols: {df_clean.shape[1]}")





#Starting Program
if __name__ == "__main__":
    Clean_311_Data(File, Output)

