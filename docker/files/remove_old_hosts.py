#!/usr/bin/python3

import pymysql
import os
import time

DB_HOST = 'database'
DB_NAME = 'patchman'
DB_USER = 'patchman'
DB_PASSWORD = 'patchman'
SELECT_QUERY_OLD_HOSTS = """SELECT hosts_host.hostname
FROM hosts_host
LEFT JOIN operatingsystems_os ON operatingsystems_os.id=hosts_host.os_id
WHERE hosts_host.lastreport < NOW() - INTERVAL 7 DAY
ORDER BY hosts_host.hostname, hosts_host.updated_at;
"""

db = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
cursor = db.cursor()

try:
    cursor.execute(SELECT_QUERY_OLD_HOSTS)
    results_old_hosts = cursor.fetchall()
    for row in results_old_hosts:
        hostname = row[0]
        os.system("/usr/bin/patchman -dh -H %s" % hostname)
        time.sleep(1)
except:
   print ("Error: unable to fetch data")
db.close()

