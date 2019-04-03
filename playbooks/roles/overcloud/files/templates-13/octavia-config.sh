#!/usr/bin/env bash

# check
crudini --get /var/lib/config-data/puppet-generated/octavia/etc/octavia/octavia.conf health_manager event_streamer_driver

# set
crudini --set /var/lib/config-data/puppet-generated/octavia/etc/octavia/octavia.conf health_manager event_streamer_driver noop_event_streamer

# apply
sudo docker restart octavia_health_manager
