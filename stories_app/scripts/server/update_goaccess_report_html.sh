#!/bin/bash

/usr/bin/zcat -f /var/log/nginx/access.log* | /usr/bin/goaccess --log-format=COMBINED --output /home/will/story-gen/stories_app/static/report.html >> /home/will/cron.log 2>&1
