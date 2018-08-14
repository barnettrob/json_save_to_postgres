import urllib2
import base64
import json
# pip install psycopg2-binary
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
    uri = apache.get('requestURI')
    remote_user = apache.get('remoteUser')
    referer_uri = apache.get('referer')
    timestamp = apache.get('timestamp')
    query = ("INSERT INTO apache_logs (request_uri, username, referer_url, timestamp, log_type) VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(query, (uri, remote_user, referer_uri, timestamp, 'apache'))
    conn.commit()
    print apache.get('requestURI')
    print apache.get('remoteUser')
    print apache.get('timestamp')