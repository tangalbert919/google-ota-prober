# Google OTA prober

This program is designed to obtain URLs to over-the-air (OTA) update packages from Google's servers for a specified device.

## Requirements
* Python 3
* Build fingerprint of your stock ROM

## How to use

You must install dependencies before using the tool: `python -m pip install -r requirements.txt`

### Option 1: Using a terminal
There are three ways to get the URL, which are listed here:
```
python probe.py --fingerprint <fingerprint>   # Skips reading config.yml entirely.
python probe.py --config <filename>           # Reads a custom YML file (same format as config.yml)
python probe.py                               # Reads config.yml
```

If you wish to download the OTA file, pass `--download` as an argument on your terminal.

### Option 2: Using a graphical interface
This option requires installing all needed modules in `requirements-gui.txt`. You must have the fingerprint for your device. The model code is optional, but encouraged.

You can run the GUI with `python gui.py`.

## Limitations
* This only works for devices that use Google's OTA update servers.
* The prober can only get the latest OTA update package that works on the build specified in `config.yml`.
* Unless it is a major Android upgrade (11 -> 12), the prober will only get links for incremental OTA packages.

## References
1. https://github.com/MCMrARM/Google-Play-API/blob/master/proto/gsf.proto
2. https://github.com/microg/GmsCore/blob/master/play-services-core-proto/src/main/proto/checkin.proto
3. https://chromium.googlesource.com/chromium/chromium/+/trunk/google_apis/gcm/protocol/android_checkin.proto
4. https://github.com/p1gp1g/fp3_get_ota_url
