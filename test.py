import os
import sys
import mysql.connector
import subprocess
import colors
import requests
from requests.exceptions import HTTPError
import urllib.request

dbName = 'craft_update_test'
dbHost = 'localhost'
dbUser = 'root'
dbPass = ''
adminEmail = "craft@oberon.nl"
adminName = "admin"
adminPass = "secret"
serverUrl = 'localhost:8000'

mydb = mysql.connector.connect(
    host=dbHost,
    user=dbUser,
    passwd=dbPass
)

mycursor = mydb.cursor()

# try:
#     colors.green("Removing database %s if it exists" % dbName)
#     mycursor.execute("DROP DATABASE %s" % dbName)
# except:
#     colors.cyan("Database %s does not yet exist" % dbName)
#
# colors.green("Creating database %s" % dbName)
# try:
#     mycursor.execute("CREATE DATABASE %s" % dbName)
# except:
#     colors.red("Could not create Database %s" % dbName)
#     sys.exit(1)
#
# # setup database config
# setupDbCmd = "php craft setup/db --interactive=0 --driver=mysql --server=\"%s\" --database=\"%s\" --user=\"%s\" --password=\"%s\"" % (dbHost, dbName, dbUser, dbPass)
#
# # install craft
# installCmd = "php craft install --interactive=0 --email=\"%s\" --username=\"%s\" --password=\"%s\" --siteName=craftTest --siteUrl=\"$SITE_URL\" --language=\"en\"" % (adminEmail, adminName, adminPass)
#
# # project sync command
# projectSyncCmd = "php craft project-config/sync"
# clearCacheCmd = "php craft clear-caches/all"
#
# colors.green("Setting up the database in .env")
# os.system(setupDbCmd)
# colors.green("Installing craft")
# os.system(installCmd)
# os.system(projectSyncCmd)
# os.system(clearCacheCmd)
# colors.green("Done installing craft")

# start php server (This should be in a docker container)

colors.green("Starting PHP server")
phpServer = subprocess.Popen(["php", "-S", serverUrl, "-t", "web/"], stdout=subprocess.PIPE, shell=True)

# perform some url calls, there should be a working installation now

url = 'http://%s/' % serverUrl

# call all existing routes
try:
    response = requests.get('%s/actions/route-map/routes/get-all-urls' % url)

    # If the response was successful, no Exception will be raised
    response.raise_for_status()
except HTTPError as http_err:
    colors.red(f'HTTP error occurred: {http_err}')
    sys.exit(1)
except Exception as err:
    colors.red(f'Other error occurred: {err}')  # Python 3.6
    sys.exit(1)
else:
    directory = 'data/'
    allLinks = response.json()
    print(response.json())
    if not os.path.exists(directory):
        os.makedirs(directory)
for link in allLinks:
    if link == '/':
        link = ''
    resp = requests.get(url + link)
    f = open(r'%s%s.txt' % (directory, link.replace("/", "_")), "w+")
    f.write(resp.content)
    f.close()

# update composer
# colors.green("Performing composer update")
# os.system('composer update')

# phpServer.terminate()
# phpServer.kill()

# colors.green("Dropping database")
# mycursor.execute("DROP DATABASE craft_update_test")
