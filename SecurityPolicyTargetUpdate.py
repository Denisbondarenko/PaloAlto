from pandevice import panorama
from pandevice import policies

# Define the variables
panorama_ip = "panorama_ip"
username = "username"
password = "password"
device_group_name = "device_group_name"
firewall_names = ["firewall1", "firewall2", "firewall3"]

# Connect to Panorama
pano = panorama.Panorama(panorama_ip, username, password)

# Select the device group
device_group = pano.device_groups[device_group_name]

# Get all Security policies in Pre Rules and Post Rules
pre_rules = device_group.pre_rules.children
post_rules = device_group.post_rules.children

# Update each rule that contains the defined firewall names
for rule in pre_rules + post_rules:
    for fw_name in firewall_names:
        if fw_name in rule.source:
            rule.source.remove(fw_name)

# Commit changes to Panorama
pano.commit(sync=True)

# Push changes to the firewalls
pano.push(sync=True)
