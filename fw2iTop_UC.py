#!/usr/bin/env python2
# FW2iTOP.py
#
# Synchronize FileWave devices to iTop CMDB (federation)
# Developed for Python 2.7.11
#
# External modules required:
#  - requests (pip install requests)
#  - ipaddress (pip install ipaddress)
#  - MySQLdb (pip install mysql-python)
#  - argparse (pip install argparse)
#  - FileWave Server (yum install -y --nogpgcheck fwxserver-<INSERT VERSION>.rpm)
#
# FileWave Consulting Engineer - dave.herder@filewave.com
# 
#https://wiki.openitop.org/doku.php?id=2_0_2:advancedtopics:data_synchronization

#import required packages 
import json
import sys
import requests
import argparse
import mysql.connector as mariadb

def main():
    # Script arguments
    description = "Synchronize FileWave devices to iTop CMDB (federation)"
#    	parser = argparse.ArgumentParser(description)
#    	parser.add_argument("-ak", "--authkey", metavar="AUTH_KEY",
#						help="FileWave Authentication key", required=True)
#		parser.add_argument("-fs", "--fwserver", metavar="FILEWAVE_SERVER",
#						help="FileWave Server", required=True)						
#    	parser.add_argument("-ih", metavar="ITOP_HOST",
#                        help="iTop server hostname", required=True)
#    	parser.add_argument("-iu", metavar="ITOP_USERNAME",
#                        help="iTop server username", required=True)
#    	parser.add_argument("-ip", metavar="ITOP_PASSWORD",
#                        help="iTop server password", required=True)
#    	parser.add_argument("-io", metavar="ITOP_ORG_ID",
#                        help="iTop organization id", required=True)
#    	parser.add_argument("-mh", metavar="MYSQL_HOST",
#                        help="iTop MySQL server hostname (optional)")
#    	parser.add_argument("-mu", metavar="MYSQL_USERNAME",
#                        help="iTop MySQL server username", required=True)
#    	parser.add_argument("-mp", metavar="MYSQL_PASSWORD",
#                        help="iTop MySQL server password", required=True)
#    	parser.add_argument("-md", metavar="MYSQL_DATABASE",
#                        help="iTop MySQL server database name", required=True)
#    	parser.add_argument("-st", metavar="SERVER_TABLE",
#                       help="iTop MySQL staging table name for Server class",
#                       required=True)
#		parser.add_argument("-pt", metavar="PRINTER_TABLE",
#                    help="iTop MySQL staging table name for Printer class",
#                    required=True)
#		parser.add_argument("-ht", metavar="HYPERVISOR_TABLE",
#                    help="iTop MySQL staging table name for Hypervisor" +
#                   " class", required=True)
#	 args = parser.parse_args()

    # Define iTop parameters interactively
#    itop_params = {}
#    itop_params["host"] = args.ih    # iTop server hostname
#    itop_params["user"] = args.iu    # iTop account
#    itop_params["password"] = args.ip    # iTop password

    # Define iTop parameters 
    itop_params = {}
    itop_params["host"] = "some.ip/itop"    # iTop server hostname
    itop_params["user"] = "username"    # iTop account
    itop_params["password"] = "password"    # iTop password

    # Define iTop MySQL DB variables
#    if args.mh is None:
#        itop_mysql_host = args.ih    # Hostname of iTop MYSQL database
#    else:
#        itop_mysql_host = args.mh
#    itop_mysql_username = args.mu    # iTop MYSQL DB account
#    itop_mysql_password = args.mp    # iTop MYSQL DB password
#    itop_mysql_db = args.md    # iTop MYSQL database name
	itop_mysql_host = 'some.ip'
	itop_mysql_username = itop    # iTop MYSQL DB account
	itop_mysql_password = itop    # iTop MYSQL DB password
	itop_mysql_db = itop    # iTop MYSQL database name

    # MySQL database for Server class; replace x with #
    #server_table = args.st
    server_table = 'ITsynchro_data_server_3'
    # MySQL database for Printer class; replace y with #
    #printer_table = args.pt
    # MySQL database for Hypervisor class; replace z with #
   	#hypervisor_table = args.ht
    
    # iTop Organization ID that all devices will be categorized with (3 = Demo)
    #itop_org_id = args.io
	itop_org_id = '3'
	
	# Define FileWave parameters interactively
#    params = {}
#    params["fwserver"] = args.fwserver
#    params["authkey"] = args.authkey
    
    #Define FileWave parameters
	url = 'https://some.randomserver.com:20443/inv/api/v1/query_result/37'
	SSL_VERIFY = False   # Ignore SSL for now
	headers = {'Authorization': 'not_the_real_key_here'}
	
	# Get JSON of Windows Server devices (testing query ID = 37)
	r = requests.get(url=url, headers=headers, verify=SSL_VERIFY)
	#print r.status_code
	#print r.headers
	#print r.encoding
	j = r.json()
	fwextract = j["values"]
	#print fwextract
	
	
	
#  Get JSON of all devices (legacy from LM script), remove when I get other stuff done
#   host_list = HostList(params)
#   j = host_list.get_hosts()

    try:
        # Setup MySQL connection
        db = MySQLdb.connect(host=itop_mysql_host,
                             user=itop_mysql_username,
                             passwd=itop_mysql_password,
                             db=itop_mysql_db)
        cur = db.cursor()

    except:
        sys.exit("ERROR: Can't connect to MySQL database.")

    print "Device(s) Added or Updated in iTop: "

    # Iterate through all Devices in portal and insert into
    # MySQL (temporary tables)
    
    
    ####################this needs to be modified to reflect my json from fw
#    for x in range(0, len(j["values"])):
#        device_id = j["values"]    # Get FW Device id from JSON
#        print device_id

		device_id = [x[1] for x in fwextract]
		#print device_id
        
        # Use the FW Device ID as the primary key in MySQL
        primary_key = device_id
		
		# Use the below code if you want to set a field in FW to extract based on. 
		# For example, set a value "itop.class" in FW for a field "properties". Useful
		# if we get re-namable custom fields.
        # Check if the "itop.class" property has been applied to the Device
# 			  if "itop.class" in j["hosts"][x]["properties"]:
#
#            itop_class = j["hosts"][x]["properties"]["itop.class"]
#            name = j["hosts"][x]["properties"]["system.displayname"]
			 name = [x[0] for x in fwextract]
#            ips = j["hosts"][x]["properties"]["system.ips"]
#            description = j["hosts"][x]["properties"]["system.sysinfo"]

            # Split string of IP addresses and assign first IP address
            # to managementip
     #       managementip = ips.split(",")[0]

            # Skip the Device if it came from iTop
     #       if "itop.source" in j["hosts"][x]["properties"]:
     #           if j["hosts"][x]["properties"]["itop.source"] == "yes":
     #               print " - " + name + " skipped."

#            elif itop_class == "Server":
                # Concatenate SQL
#                sql = "INSERT INTO " + server_table +\
#                      " (primary_key, name, description, org_id, man" +\
#                      "agementip) VALUES ({0}, \"{1}\", \"{2}\", " +\
#                      itop_org_id + ", \"{3}\")"

#                cur.execute(sql.format(primary_key, name, description,
#                                       managementip))
                                       
                                       
                sql = "INSERT INTO " + server_table +\
                      " (primary_key, name) VALUES ({1}, \"{0}\")"

                cur.execute(sql.format(primary_key, name))
                db.commit()
                print " - " + name

    #        elif itop_class == "Printer":
                # Concatenate SQL
    #            sql = "INSERT INTO " + printer_table +\
    #                  " (primary_key, name, description, org_id) VALUES " +\
    #                  "({0}, \"{1}\", \"{2}\", " + itop_org_id + ")"
    #            cur.execute(sql.format(primary_key, name, description))
    #            db.commit()
    #            print " - " + name

    #        elif itop_class == "Hypervisor":
                # Concatenate SQL
    #            sql = "INSERT INTO " + hypervisor_table +\
    #                  " (primary_key, name, description, org_id) VALUES " +\
    #                  "({0}, \"{1}\", \"{2}\", " + itop_org_id + ")"
    #            cur.execute(sql.format(primary_key, name, description))
    #            db.commit()
    #            print " - " + name

    # Execute iTop PHP script to insert MySQL temporary table data into
    # CMDB (create or update). Concatenate URL to PHP script
    url_sync = "http://" + itop_params["host"] +\
               "/web/synchro/synchro_exec.php"

    # Get the last character of each table, which provides the data_source #
    # Build comma-separate string to use in URL payload.
    ds_value = server_table[-1:]
    #ds_value = server_table[-1:] + "," + printer_table[-1:] + "," +\
    #                               hypervisor_table[-1:]
    payload = {"data_sources": ds_value}

    # Remotely execute iTop PHP script
    requests.get(url_sync, auth=(itop_params["user"],
                                 itop_params["password"]), params=payload)

    # Empty MySQL tables
    sql = "TRUNCATE TABLE " + server_table
    cur.execute(sql)
    #sql = "TRUNCATE TABLE " + printer_table
    #cur.execute(sql)
    #sql = "TRUNCATE TABLE " + hypervisor_table
    #cur.execute(sql)
    db.commit()
    db.close()

main()

