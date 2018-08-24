import urllib2
import base64
import json
# sudo pip install psycopg2-binary
import psycopg2

username = 'user1'
password = 'xxxxxxx'
url = 'http://mydomain.com/api/rest/values.json'
base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

request = urllib2.Request(url)

request.add_header("Authorization", "Basic %s" % base64string)

result = urllib2.urlopen(request)
data = json.load(result)

# Database information inserting apache logs into.
dbhost= 'localhost'
dbuser = 'dbuser'
dbpass = 'dbpassword'
database = 'mydb'

# port is 5432 by default.  So if different then specify port.
conn = psycopg2.connect(dbname=database, user=dbuser, host=dbhost, password=dbpass, port='32771')
cursor = conn.cursor()

# Second database information for getting additional data to insert back into apache logs first database above.
w_dbhost = 'localhost' # this will not be localhost for production setup.
w_dbuser = 'dbuser2'
w_dbpass = 'dpassword2'
w_database = 'mydb2'

website_conn = psycopg2.connect(dbname=w_database, user=w_dbuser, host=w_dbhost, password=w_dbpass, port='32771')
w_cursor = website_conn.cursor()

# use get() to account for missing keys.
for event in data['events']:
    event = event.get('event')
    apache = event.get('apache')
    syslog = event.get('syslog')

    referer_uri = apache.get('referer')
    remote_user = apache.get('remoteUser')
    request_method = apache.get('requestMethod')
    request_protocol = apache.get('requestProtocol')
    request_uri = apache.get('requestURI')
    size = apache.get('size')
    status = apache.get('status')
    timestamp = apache.get('timestamp')
    user_agent = apache.get('userAgent')
    app_name = syslog.get('appName')
    facility = syslog.get('facility')
    host = syslog.get('host')
    priority = syslog.get('priority')
    severity = syslog.get('severity')

    query = ("INSERT INTO apache_logs (referer, remote_user, request_method, request_protocol, request_uri, size, status, timestamp, user_agent, app_name, facility, host, priority, severity)"
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (referer_uri, remote_user, request_method, request_protocol, request_uri, size, status, timestamp, user_agent, app_name, facility, host, priority, severity))
    conn.commit()

    # Get company from website database.
    if remote_user is not None:
        website_query = "SELECT field_company_value FROM field_data_field_company co LEFT JOIN users u ON co.entity_id = u.uid WHERE u.name = %s"
        w_cursor.execute(website_query, (remote_user,))
        w_row = w_cursor.fetchone()
        company = w_row[0]

    # Update record from apache log postgres
        if company or company is not None:
            update_w_company_query = ("UPDATE apache_logs SET domain = %s WHERE remote_user = %s AND timestamp = %s")
            cursor.execute(update_w_company_query, (company, remote_user, timestamp))
            conn.commit()

    print apache.get('requestURI')
    print apache.get('remoteUser')
    print apache.get('timestamp')