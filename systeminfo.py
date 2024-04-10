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
import sys
import re

if __name__ == '__main__':

  try:

    #---------------------------------------------------------------------------------------------------------------------------------------------------
    # This is the section where you can set user , password , command , os_filter and firewall_list.
    api_user      = "PUT_YOUR_USERNAME_HERE"
    api_password  = "PUT_YOUR_PASSWORD_HERE"
    firewalls     = [["PUT_FW1_HOSTNAME_HERE","PUT_FW1_IP_HERE"], 
                     ["PUT_FW2_HOSTNAME_HERE","PUT_FW2_IP_HERE"], 
                     ["PUT_FW3_HOSTNAME_HERE","PUT_FW3_IP_HERE"], 
                     ["PUT_FW4_HOSTNAME_HERE","PUT_FW4_IP_HERE"]]

    command             = "show system info"
    uptime_filter       = "<uptime>(.*)</uptime>"
    model_filter        = "<model>(.*)</model>"
    
    #---------------------------------------------------------------------------------------------------------------------------------------------------
    # This is the section  where the framework connect to the firewalls to execute the command and display the result.
  
    for firewall_name, firewall_ip in firewalls:
      firewall_connect = firewall.Firewall(hostname=firewall_ip, api_username=api_user, api_password=api_password)
      system_info      = firewall_connect.op(cmd=command, xml=True)

      #un-comment the line below to see the full ouput of the operational command
      #print(system_info)

      uptime           = re.search(uptime_filter,str(system_info))
      model            = re.search(model_filter,str(system_info))

      print(firewall_name+" - uptime: "+uptime.group(1)+" - model: "+model.group(1))
    #---------------------------------------------------------------------------------------------------------------------------------------------------

  except:
    print("ERROR   : Connecting to "+firewall_ip+". Check the Firewall IP address and Credentials.")
    sys.exit(0)	