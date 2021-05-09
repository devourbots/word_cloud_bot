#! /bin/sh \
cd /root/word_cloud_bot && python3 main.py >> output 2>&1 &
tail -f /dev/null