# sudo pip install wheel
# sudo pip install tornado
# sudo pip install nose
# sudo pip install pandas
# sudo pip install sqlalchemy
import pandas as pd
from sqlalchemy import create_engine

conn = create_engine('postgresql+psycopg2://user:password@host:port/dbname')

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
TO_TIMESTAMP(downloadtime) AS downloadtime
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
    # process  'result_chunk' (chunk of 10,000 rows) here
    if i == 2:
        break
    print result_chunk

