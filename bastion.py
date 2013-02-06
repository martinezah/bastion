#!/usr/bin/env python

import sys
import math
import json
from datetime import datetime
from boto.ec2.connection import EC2Connection

def backup(vol, sys, scheme):
    if (stamp.hour % scheme["period"] == 0):
        nickname = '{}_{}_{}'.format(sys, vol.id, stamp.isoformat())
        print "Creating Snapshot:", nickname
        ec2.create_snapshot(vol.id, nickname)
        snap_list = vol.snapshots()
        snap_list.sort(lambda x, y: int(math.ceil((datetime.strptime(x.start_time, "%Y-%m-%dT%H:%M:%S.%fZ") - datetime.strptime(y.start_time, "%Y-%m-%dT%H:%M:%S.%fZ")).total_seconds())), reverse = True)
        weekly = scheme["retention"]["weekly"]
        daily  = scheme["retention"]["daily"]
        hourly = scheme["retention"]["hourly"]
        for snap in snap_list:
            when = datetime.strptime(snap.start_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            if (when.weekday() == 0):
                if (weekly > 0):
                    weekly -= 1
                else:
                    print "Deleting Snapshot:", snap.description
                    snap.delete()
            elif (when.hour == 0):
                if (daily > 0):
                    daily -= 1
                else:
                    print "Deleting Snapshot:", snap.description
                    snap.delete()
            else:
                if (hourly):
                    hourly -= 1
                else:
                    print "Deleting Snapshot:", snap.description
                    snap.delete()

stamp = datetime.now()
try: 
    config = json.load(open(sys.argv[1]))
except IndexError:
    print "usage: {} config.json".format(sys.argv[0])
    sys.exit(1)
except ValueError as e:
    print "Failed parsing config file: {}".format(sys.argv[1])
    print e
    sys.exit(1)

ec2 = EC2Connection(config["credentials"]["AWS_ACCESS_KEY_ID"],config["credentials"]["AWS_SECRET_ACCESS_KEY"])
res_list = ec2.get_all_instances()
vol_list = ec2.get_all_volumes()

for sys,scheme in config["instances"].items():
    for res in res_list:
        for inst in res.instances:
            if (inst.id == sys or inst.__dict__['tags']['Name'] == sys):
                for vol in vol_list:
                    if (vol.attach_data.instance_id == inst.id):
                        backup(vol, sys, config["schemes"][scheme]) 
