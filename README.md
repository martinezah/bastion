bastion
=======

EC2 Rotating Backup Framework

Bastion is a simple framework for automating backup rotations of EC2 volumes. It allows your to specify multiple backup rotation schemes, and apply those to the servers in your infrastructure. A cron job manages the creation of snapshots as well as rotation of older backups to offline storage (AWS Glacier) and purging of old backups.

Configuration
-------

Configuration is managed through a simple json file, with three sections. A sample configuration file, sample-config.json, is included. The first section, "credentials", holds the AWS credentials used to access the EC2 and Glacier API. The second, "schemes", describes the available backup rotation schemes, and the third, "instances", maps EC2 instances to the appropriate schemes. Instances can be referred to by their instance ID, or by their "Name" tag if one has been assigned in AWS.

Deployment
-------

Bastion is designed to be run as an hourly cron job.  The minimal invocation syntax (assuming the config file is called config.json) is:

bastion.py config.json

My primary deployment, via puppet, looks like this:

# Puppet Name: AWS Backups
5 * * * * /bin/bash -c 'cd /opt/bastion ; ./bastion.py config.json' >> /var/log/bastion.log

