#!/usr/bin/python3

from checkin import checkin_generator_pb2
from google.protobuf import text_format
from utils import functions
import argparse, requests, gzip, yaml

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true', help='Print debug information to text file.')
parser.add_argument('--download', action='store_true', help='Download the OTA file.')
parser.add_argument('--fingerprint', help='Get the OTA using this fingerprint. Reading the config YML file is skipped.')
parser.add_argument('--model', help='Specify the model of the device. If not specified, the device code will be used.')
parser.add_argument('--config', help='Use this config file instead of the default one.', default='config.yml')
args = parser.parse_args()

class Prober:
    def __init__(self):
        self.checkinproto = checkin_generator_pb2.AndroidCheckinProto()
        self.payload = checkin_generator_pb2.AndroidCheckinRequest()
        self.build = checkin_generator_pb2.AndroidBuildProto()
        self.response = checkin_generator_pb2.AndroidCheckinResponse()

    def get_update_desc(self):
        setting = {entry.name: entry.value for entry in self.response.setting}
        update_desc = setting.get(b'update_description', b'').decode()
        return update_desc

    def checkin(self, fingerprint: str, model: str = None, debug: bool = False) -> str:
        self.checkinproto.Clear()
        self.payload.Clear()
        self.build.Clear()
        self.response.Clear()

        try:
            config = fingerprint.split('/')
            # Split "<device>:<android_version">
            temp = config[2].split(':')
            # Drop, then reinsert as two separate entries
            config.pop(2)
            config.insert(2, temp[0])
            config.insert(3, temp[1])
            current_build = config[4]
            android_version = config[3]
            device = config[2]
        except:
            print("Invalid fingerprint.")
            return None
        if model is None or model == '':
            model = device
        self.headers = {
            'accept-encoding': 'gzip, deflate',
            'content-encoding': 'gzip',
            'content-type': 'application/x-protobuffer',
            'user-agent': f'Dalvik/2.1.0 (Linux; U; Android {android_version}; {model} Build/{current_build})'
        }

        # Add build properties
        self.build.id = fingerprint
        self.build.timestamp = 0
        self.build.device = device

        # Checkin proto
        self.checkinproto.build.CopyFrom(self.build)
        self.checkinproto.lastCheckinMsec = 0
        self.checkinproto.roaming = "WIFI::"
        self.checkinproto.userNumber = 0
        self.checkinproto.deviceType = 2
        self.checkinproto.voiceCapable = False
        self.checkinproto.unknown19 = "WIFI"

        # Generate the payload
        self.payload.imei = functions.generateImei()
        self.payload.id = 0
        self.payload.digest = functions.generateDigest()
        self.payload.checkin.CopyFrom(self.checkinproto)
        self.payload.locale = 'en-US'
        self.payload.macAddr.append(functions.generateMac())
        self.payload.timeZone = 'America/New_York'
        self.payload.version = 3
        self.payload.serialNumber = functions.generateSerial()
        self.payload.macAddrType.append('wifi')
        self.payload.fragment = 0
        self.payload.userSerialNumber = 0
        self.payload.fetchSystemUpdates = 1
        self.payload.unknown30 = 0

        with gzip.open('test_data.gz', 'wb') as f_out:
            f_out.write(self.payload.SerializeToString())
            f_out.close()

        post_data = open('test_data.gz', 'rb')
        r = requests.post('https://android.googleapis.com/checkin', data=post_data, headers=self.headers)
        post_data.close()

        download_url = ""
        try:
            self.response.ParseFromString(r.content)
            if debug:
                with open('debug.txt', 'w') as f:
                    f.write(text_format.MessageToString(self.response))
                    f.close()
            setting = {entry.name: entry.value for entry in self.response.setting}
            update_title = setting.get(b'update_title', b'').decode()
            if update_title:
                print("Update title: " + setting.get(b'update_title', b'').decode())
            download_url = setting.get(b'update_url', b'').decode()
            if download_url:
                print("OTA URL obtained: " + download_url)
                return download_url
            else:
                print("No OTA URL found for your build. Either Google does not recognize your build fingerprint, or there are no new updates for your device.")
            return None
        except:
            print("Invalid fingerprint.")
            return None

    def checkin_cli(self) -> str:
        if args.fingerprint:
            return self.checkin(args.fingerprint, args.model, args.debug)
        else:
            try:
                with open(args.config, 'r') as file:
                    config = yaml.safe_load(file)
                    file.close()
                return self.checkin(f'{config["oem"]}/{config["product"]}/{config["device"]}:{config["android_version"]}/{config["build_tag"]}/{config["incremental"]}:user/release-keys', config['model'], args.debug)
            except:
                print("Invalid config file.")
                exit(1)
        
    def download(self, url: str, progress_bar = None, page = None) -> None:
        if url is None:
            return
        print("Downloading OTA file")
        with requests.get(url, stream=True) as resp:
            resp.raise_for_status()
            filename = url.split('/')[-1]

            total_size = int(resp.headers.get('content-length', 0))
            chunk_size = 1024

            with open(filename, 'wb') as file:
                progress = 0

                for chunk in resp.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
                        progress += len(chunk)
                        if progress_bar is not None and page is not None:
                            progress_bar.value = float(progress / total_size)
                            page.update()
                        percentage = (progress / total_size) * 100
                        print(f"Downloaded {progress} of {total_size} bytes ({percentage:.2f}%)", end="\r")
            print(f"File downloaded and saved as {filename}!")


if __name__ == '__main__':
    prober = Prober()
    if args.download:
        prober.download(prober.checkin_cli())
    else:
        prober.checkin_cli()