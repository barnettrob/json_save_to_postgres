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

dbhost= 'localhost'
dbuser = 'dbuser'
dbpass = 'dbpassword'
database = 'mydb'

# port is 5432 by default.  So if different then specify port.
conn = psycopg2.connect(dbname=database, user=dbuser, host=dbhost, password=dbpass, port='32771')

cursor = conn.cursor()

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

    print apache.get('requestURI')
    print apache.get('remoteUser')
    print apache.get('timestamp')