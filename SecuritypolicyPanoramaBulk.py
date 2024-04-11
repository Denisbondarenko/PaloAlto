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

from pandevice import panorama
from pandevice import objects
from pandevice import policies
import sys
import csv

if __name__ == '__main__':

  try:
    #---------------------------------------------------------------------------------------------------------------------------------------------------
    # This is the section where you can set your api_key , uri and path of the CSV file
    api_user       = "PUT_YOUR_USERNAME_HERE"
    api_password   = "PUT_YOUR_PASSWORD_HERE"
    panorama_ip    = "PUT_YOUR_PANORAMA_IP_HERE"
    rule_file      = "SampleRuleFile.csv"
    #---------------------------------------------------------------------------------------------------------------------------------------------------

    panorama_prod  = panorama.Panorama(hostname=panorama_ip, api_username=api_user, api_password=api_password)
    # Panorama -> Device-Group
    device_group   = panorama.DeviceGroup("production")
    panorama_prod.add(device_group)
    # Panorama -> Device-Group -> Post Rules
    rulebase       = policies.PostRulebase()
    device_group.add(rulebase)

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


    # Panorama -> Device-Group -> Post Rules -> Security Rules
    rulebase.extend(security_rules)
    # Find every object at the same level than 'rule_1' and create it.
    rulebase.find('rule_1').create_similar()
  
    panorama_prod.commit()

  except:
    print("ERROR   :  Check the IP address and credentials. Make sure the PATH of the CSV file is correct.")
    sys.exit(0)	
























































































































































































































































































































































































































































































# Copyright (c) 2017, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
