#!/usr/bin/env python

import sys
import json
from boto.ec2.connection import EC2Connection

def backup(vol, sys, scheme):
    print "Found", vol.id, "on", sys, "launching", scheme, "backup"
    print config["schemes"][scheme]

config_file = sys.argv[1]
config = json.load(open(config_file))

conn = EC2Connection(config["credentials"]["AWS_ACCESS_KEY_ID"],config["credentials"]["AWS_SECRET_ACCESS_KEY"])
res_list = conn.get_all_instances()
vol_list = conn.get_all_volumes()

for sys,scheme in config["instances"].items():
    for res in res_list:
        for inst in res.instances:
            if (inst.id == sys or inst.__dict__['tags']['Name'] == sys):
                for vol in vol_list:
                    if (vol.attach_data.instance_id == inst.id):
                        backup(vol, sys, scheme) 
