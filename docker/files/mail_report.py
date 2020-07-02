#!/usr/bin/python3

import pymysql
import smtplib
from email.mime.text import MIMEText

MAIL_FROM = 'Patchman <patchman@example.com>'
MAIL_TO = 'Receiver <to@example.com>'
MAIL_CC = 'Copy To <cc@@example.com>'

DB_HOST = 'database'
DB_NAME = 'patchman'
DB_USER = 'patchman'
DB_PASSWORD = 'patchman'
SELECT_QUERY_PENDING_REBOOT = """SELECT hosts_host.hostname,
       DATE_FORMAT(hosts_host.updated_at, "%Y-%m-%d"),
       operatingsystems_os.name
FROM hosts_host
LEFT JOIN operatingsystems_os ON operatingsystems_os.id=hosts_host.os_id
WHERE reboot_required = 1
ORDER BY hosts_host.hostname, hosts_host.updated_at;
"""
MAIL_TEXT = """<h3>Please find below instances which pending reboot</h3>
<table>
<tr><th>Hostname</th><th>OS Name</th><th>Report Date</th></tr>
"""

db = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
cursor = db.cursor()

try:
    cursor.execute(SELECT_QUERY_PENDING_REBOOT)
    results_pending_reboot = cursor.fetchall()
    for row in results_pending_reboot:
        hostname = row[0]
        updated_at = row[1]
        os_name = row[2]
        MAIL_TEXT += "<tr><td>%s</td><td style=\"text-align:center\">%s</td><td style=\"text-align:center\">%s</td></tr>\n" % (hostname, os_name, updated_at)
except:
   print ("Error: unable to fetch data")
MAIL_TEXT += "</table>\n"
db.close()

message = MIMEText(MAIL_TEXT, 'html')
message['From'] = MAIL_FROM
message['To'] = MAIL_TO
message['Cc'] = MAIL_CC
message['Subject'] = '[Patchman] Hosts with pending reboot status'

smtp_server = smtplib.SMTP('smtp.example.com:25')
smtp_server.starttls()
smtp_server.login('smtp_user', 'smtp_credentials')
smtp_server.sendmail(MAIL_FROM, [MAIL_TO, MAIL_CC], message.as_string())
smtp_server.quit()

