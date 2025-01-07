import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

# Import CID IDS Dataframe
df = pd.read_csv("C:/Users/arin1/Google Drive/FaPra_SW_Entw/CIC_IDS_2017/data_renamed.csv")


# Replace with your PostgreSQL connection details
username = 'postgres'
password = 'example'
host = 'localhost'
port = "5432"
database = 'data'

# Create the connection string
connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'

# Create the SQLAlchemy engine
engine = create_engine(connection_string)

# Name of the table in PostgreSQL
table_name = 'network_flows'

# Add DataFrame to PostgreSQL
#df.to_sql(table_name, engine, if_exists='replace', index=False)

# Query the database
with engine.connect() as connection:
    query = text(f"SELECT * FROM {table_name}")
    result = connection.execute(query)
    for row in result:
        print(row)