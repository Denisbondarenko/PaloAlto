#!/usr/bin/env python
# Copyright (c) 2017, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from pandevice import firewall
from pandevice import objects
from pandevice import policies
import timeit
import csv
import sys

if __name__ == '__main__':
  
  try: 

    #---------------------------------------------------------------------------------------------------------------------------------------------------
    # This is the section where you can set your api_key , uri and path of the CSV file
    api_user       = "PUT_YOUR_USERNAME_HERE"
    api_password   = "PUT_YOUR_PASSWORD_HERE"
    firewall_ip    = "PUT_YOUR_FW_IP_HERE"
    rule_file      = "lab9-rules.csv"

    #---------------------------------------------------------------------------------------------------------------------------------------------------
    firewall = firewall.Firewall(hostname=firewall_ip, api_username=api_user, api_password=api_password)

    # The following configuration Tree will be created : Firewall -> Rule Base -> Security Rule
    # Create an empty rulebase container. 
    rulebase = policies.Rulebase()
    # Add the empty rulebase container to the configuration Tree. 
    # Firewall -> Rule Base
    firewall.add(rulebase)

    file_      = open(rule_file, 'r')
    csv_reader = csv.reader(file_)
    security_rules = []

    for row in csv_reader:   
      #-----------------------------------------------------------------------------------------------------------
      # In the CSV file, row[0] is the value of rule name
      # In the CSV file, row[1] is the value of the source zone ( any )
      # In the CSV file, row[2] is the value of the source IP
      # In the CSV file, row[3] is the value of destination zone ( any )
      # In the CSV file, row[4] is the value of the destination IP
      # In the CSV file, row[5] is the value of the application
      # In the CSV file, row[6] is the value of the service 
      # In the CSV file, row[7] is the value of the action

        rule_name         = row[0]
        source_zone       = row[1].split(" ")
        source_ip         = row[2].split(" ")   
        destination_zone  = row[3].split(" ")    
        destination_ip    = row[4].split(" ")    
        application       = row[5].split(" ")    
        service           = row[6].split(" ")   
        action            = row[7] 

        security_rules.append(policies.SecurityRule(name=rule_name, fromzone=source_zone, source=source_ip, tozone=destination_zone,  destination=destination_ip, application=application, service=service, action=action))
    
    # Add the rule LIST  to the RuleBase container. 
    # Firewall -> Rule Base -> Security Rule  
    rulebase.extend(security_rules)

    # Find every object at the same level than 'rule_1' and create it.
    rulebase.find('rule_1').create_similar()
    firewall.commit()

  except:
    print("ERROR   :  Check the IP address and credentials. Make sure the PATH of the CSV file is correct.")
    sys.exit(0)	
