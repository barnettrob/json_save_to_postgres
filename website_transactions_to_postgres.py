# sudo pip install wheel
# sudo pip install tornado
# sudo pip install nose
# sudo pip install pandas
# sudo pip install sqlalchemy
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

conn = create_engine('postgresql+psycopg2://user:password@host:port/dbname')

# transaction postgres database.
transaction_dbhost = 'localhost'
transaction_dbuser = 'xxxxx'
transaction_dbpass = 'xxxxx'
transaction_database = 'transactions'

# port is 5432 by default.  So if different then specify port.
t_conn = psycopg2.connect(dbname=transaction_database, user=transaction_dbuser, host=transaction_dbhost, password=transaction_dbpass, port='32771')
t_cursor = t_conn.cursor()

# Query edb transaction logs from website drupal_d7_latest
query = """SELECT n.title AS product_name,
field_product_group_value AS product_group,
field_resource_uri_url AS transaction,
transactionid,
(CASE WHEN CONCAT(field_first_name_value, ' ', field_last_name_value) = ' ' THEN
'Anonymous'
ELSE
CONCAT(field_first_name_value, ' ', field_last_name_value)
END) AS name,
(CASE WHEN field_company_value IS NULL THEN
'Anonymous'
ELSE
field_company_value
END) AS company,
u.mail AS email, userip,
downloadtime, 'drupal_d7_latest' AS database_origin
FROM edb_transaction_log etl
LEFT JOIN users u ON CAST(etl.userid AS INT) = u.uid
LEFT JOIN field_data_field_company c ON u.uid = c.entity_id
LEFT JOIN field_data_field_first_name f ON u.uid = f.entity_id
LEFT JOIN field_data_field_last_name l ON u.uid = l.entity_id
LEFT JOIN node n ON etl.assetid = n.nid
LEFT JOIN field_data_field_resource_uri r ON n.nid = r.entity_id
LEFT JOIN field_data_field_product_group pg ON n.nid = pg.entity_id
WHERE TO_TIMESTAMP(downloadtime)::DATE >= DATE '2017-01-01'"""

results = pd.read_sql(query, con=conn, chunksize = 10**4)

for i, result_chunk in enumerate(results):
    # Process  'result_chunk' (chunk of 10,000 rows) here
    # if i == 2:
    #     break
    # Convert result_chunk the pandas series to array of tuples.
    tuples = [tuple(x) for x in result_chunk.values]
    t_query = ("INSERT INTO website_transactions (product_name, product_group, transaction, transactionid, name, company, email, userip, downloadtime, database_origin)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    t_cursor.executemany(t_query, tuples)
    t_conn.commit()