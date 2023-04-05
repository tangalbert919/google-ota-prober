#!/usr/bin/python3

import requests

# Fill this in with the information you need
current_build = 'RKQ1.201217.002'
current_incremental = '2302071508'
security_patch = '2023-02-05'
android_version = '11'
current_model = 'BE2011'

headers = {
    'accept-encoding': 'gzip, deflate',
    'content-encoding': 'gzip',
    'content-type': 'application/x-protobuffer',
    'user-agent': f'Dalvik/2.1.0 (Linux; U; Android {android_version}; {current_model} Build/{current_build})'
}
post_data = open('post_data.gz', 'rb')
r = requests.post('https://android.googleapis.com/checkin', data=post_data, headers=headers)
print(r.text)
print(r.headers)
