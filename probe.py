#!/usr/bin/python3

from checkin import checkin_generator_pb2
from utils import functions
import requests
import gzip
import random
import shutil
import os
import binascii
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

current_build = config['build_tag']
current_incremental = config['incremental']
android_version = config['android_version']
model = config['model']
device = config['device']
oem = config['oem']
product = config['product']

headers = {
    'accept-encoding': 'gzip, deflate',
    'content-encoding': 'gzip',
    'content-type': 'application/x-protobuffer',
    'user-agent': f'Dalvik/2.1.0 (Linux; U; Android {android_version}; {model} Build/{current_build})'
}

checkinproto = checkin_generator_pb2.AndroidCheckinProto()
payload = checkin_generator_pb2.AndroidCheckinRequest()
build = checkin_generator_pb2.AndroidBuildProto()
response = checkin_generator_pb2.AndroidCheckinResponse()

# Add build properties
build.id = f'{oem}/{product}/{device}:{android_version}/{current_build}/{current_incremental}:user/release-keys' # Put the build fingerprint here
build.timestamp = 0
build.device = device

# Checkin proto
checkinproto.build.CopyFrom(build)
checkinproto.lastCheckinMsec = 0
checkinproto.roaming = "WIFI::"
checkinproto.userNumber = 0
checkinproto.deviceType = 2
checkinproto.voiceCapable = False
checkinproto.unknown19 = "WIFI"

# Generate the payload
payload.imei = functions.generateImei()
payload.id = 0
payload.digest = functions.generateDigest()
payload.checkin.CopyFrom(checkinproto)
payload.locale = 'en-US'
payload.loggingId = int(random.random() * 1000000000)
payload.macAddr.append(functions.generateMac())
payload.timeZone = 'America/New_York'
payload.version = 3
payload.serialNumber = functions.generateSerial()
payload.macAddrType.append('wifi')
payload.fragment = 0
payload.userSerialNumber = 0
payload.fetchSystemUpdates = 1
payload.unknown30 = 0

with open('test_data.txt', 'wb') as f:
    f.write(payload.SerializeToString())
    f.close()

with open('test_data.txt', 'rb') as f_in:
    with gzip.open('test_data.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

post_data = open('test_data.gz', 'rb')
r = requests.post('https://android.googleapis.com/checkin', data=post_data, headers=headers)
with open('test_response', 'wb') as result:
    result.write(r.content)
    result.close()

with open('test_response', 'rb') as f:
    response.ParseFromString(f.read())
    for entry in response.setting:
        if b'https://android.googleapis.com' in entry.value:
            print("OTA URL obtained: " + entry.value.decode())
#print(r.text)
#print(r.headers)
