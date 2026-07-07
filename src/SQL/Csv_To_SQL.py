import pandas as pd
import sqlalchemy as sa
from pathlib import Path
import os

# To view SQLite in VS Code: https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer
# If the data is too large you can also use Pandas to read it. Look at ReadingSQLite.ipynb for more info.
# If using a Database make sure to keep login information in an .env file.

ProjectRoot = Path(__file__).resolve().parent.parent.parent

csvFileLocation = ProjectRoot / 'data' / 'Clean' / 'New_Data.csv'
SQLiteFile = ProjectRoot / 'data' / '311NYC_OpenData.db' # If none it will be made for you.


# Making an SQLite File.
SQLiteFile.touch(exist_ok=True)

#print(csvFile)

engine = sa.create_engine(f"sqlite:///{SQLiteFile}")

df = pd.read_csv(csvFileLocation)

df.to_sql("service_requests", engine, if_exists="replace", index=False)


