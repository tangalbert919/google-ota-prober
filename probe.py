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
security_patch = '2022-11-05'
android_version = config['android_version']
model = config['model']
device = config['device']
oem = config['oem']
product = config['product']
radio = ''

headers = {
    'accept-encoding': 'gzip, deflate',
    'content-encoding': 'gzip',
    'content-type': 'application/x-protobuffer',
    'user-agent': f'Dalvik/2.1.0 (Linux; U; Android {android_version}; {model} Build/{current_build})'
}

checkinproto = checkin_generator_pb2.AndroidCheckinProto()
payload = checkin_generator_pb2.AndroidCheckinRequest()
devicefeature = checkin_generator_pb2.DeviceFeature()
deviceconfig = checkin_generator_pb2.DeviceConfigurationProto()
statistics = checkin_generator_pb2.AndroidStatisticProto()
events = checkin_generator_pb2.AndroidEventProto()
build = checkin_generator_pb2.AndroidBuildProto()
reason = checkin_generator_pb2.AndroidCheckinReasonProto()

# Add build properties
build.id = f'{oem}/{product}/{device}:{android_version}/{current_build}/{current_incremental}:user/release-keys' # Put the build fingerprint here
build.hardware = 'qcom'
build.brand = oem
build.radio = radio
build.bootloader = 'unknown'
build.clientId = f'android-{oem.lower()}' # Usually "android-<oem>", e.g. android-oneplus
build.timestamp = 0
build.googleServices = 8768315 # Actually version code for google services framework
build.device = device
build.sdkVersion = 30
build.model = model
build.manufacturer = oem
build.product = product
build.otaInstalled = False
group_main = build.groups.add()
group_main.version = 1
group_main.name = f'android-{oem.lower()}'
group_ms = build.groups.add()
group_ms.version = 2
group_ms.name = f'ms-android-{oem.lower()}'
group_gmm = build.groups.add()
group_gmm.version = 4
group_gmm.name = f'gmm-android-{oem.lower()}'
group_mvapp = build.groups.add()
group_mvapp.version = 5
group_mvapp.name = f'mvapp-android-{oem.lower()}'
group_am = build.groups.add()
group_am.version = 6
group_am.name = f'am-android-{oem.lower()}'
group_ms2 = build.groups.add()
group_ms2.version = 9
group_ms2.name = f'ms-android-{oem.lower()}'
build.securityPatch = security_patch

# Checkin proto
checkinproto.build.CopyFrom(build)
checkinproto.lastCheckinMsec = 0
event = checkinproto.event.add()
event.tag = 'event_log_start'
event.timeMsec = 0
checkinproto.roaming = "WIFI::"
checkinproto.userNumber = 0
checkinproto.deviceType = 2

# Reason proto
reason.reasonType = 1
reason.attemptCount = 1
reason.sourcePackage = "com.google.android.gms"
reason.sourceForce = False

checkinproto.reason.CopyFrom(reason)
checkinproto.voiceCapable = False
checkinproto.unknown19 = "WIFI"

# Device configuration
deviceconfig.touchScreen = 3
deviceconfig.keyboard = 1
deviceconfig.navigation = 1
deviceconfig.screenLayout = 2
deviceconfig.hasHardKeyboard = False
deviceconfig.hasFiveWayNavigation = False
deviceconfig.screenDensity = 320
deviceconfig.glEsVersion = 131072
#deviceconfig.systemSharedLibrary.append()
deviceconfig.systemAvailableFeature.extend(["android.hardware.bluetooth",
                    "android.hardware.camera",
                    "android.hardware.camera.autofocus",
                    "android.hardware.camera.flash",
                    "android.hardware.camera.front",
                    "android.hardware.faketouch",
                    "android.hardware.location",
                    "android.hardware.location.gps",
                    "android.hardware.location.network",
                    "android.hardware.microphone",
                    "android.hardware.nfc",
                    "android.hardware.screen.landscape",
                    "android.hardware.screen.portrait",
                    "android.hardware.sensor.accelerometer",
                    "android.hardware.sensor.barometer",
                    "android.hardware.sensor.compass",
                    "android.hardware.sensor.gyroscope",
                    "android.hardware.sensor.light",
                    "android.hardware.sensor.proximity",
                    "android.hardware.telephony",
                    "android.hardware.telephony.gsm",
                    "android.hardware.touchscreen",
                    "android.hardware.touchscreen.multitouch",
                    "android.hardware.touchscreen.multitouch.distinct",
                    "android.hardware.touchscreen.multitouch.jazzhand",
                    "android.hardware.usb.accessory",
                    "android.hardware.usb.host",
                    "android.hardware.wifi",
                    "android.hardware.wifi.direct",
                    "android.software.live_wallpaper",
                    "android.software.sip",
                    "android.software.sip.voip",
                    "com.google.android.feature.GOOGLE_BUILD",
                    "com.nxp.mifare"])
deviceconfig.nativePlatform.extend(['arm64-v8a', 'armeabi-v7a', 'armeabi'])
deviceconfig.systemSupportedLocale.extend(["af", "af_ZA", "am", "am_ET", "ar", "ar_EG", "bg", "bg_BG",
                    "ca", "ca_ES", "cs", "cs_CZ", "da", "da_DK", "de", "de_AT",
                    "de_CH", "de_DE", "de_LI", "el", "el_GR", "en", "en_AU",
                    "en_CA", "en_GB", "en_NZ", "en_SG", "en_US", "es", "es_ES",
                    "es_US", "fa", "fa_IR", "fi", "fi_FI", "fr", "fr_BE",
                    "fr_CA", "fr_CH", "fr_FR", "hi", "hi_IN", "hr", "hr_HR",
                    "hu", "hu_HU", "in", "in_ID", "it", "it_CH", "it_IT", "iw",
                    "iw_IL", "ja", "ja_JP", "ko", "ko_KR", "lt", "lt_LT", "lv",
                    "lv_LV", "ms", "ms_MY", "nb", "nb_NO", "nl", "nl_BE",
                    "nl_NL", "pl", "pl_PL", "pt", "pt_BR", "pt_PT", "rm",
                    "rm_CH", "ro", "ro_RO", "ru", "ru_RU", "sk", "sk_SK", "sl",
                    "sl_SI", "sr", "sr_RS", "sv", "sv_SE", "sw", "sw_TZ", "th",
                    "th_TH", "tl", "tl_PH", "tr", "tr_TR", "ug", "ug_CN", "uk",
                    "uk_UA", "vi", "vi_VN", "zh_CN", "zh_TW", "zu", "zu_ZA"])
deviceconfig.glExtension.extend(["GL_EXT_debug_marker",
                    "GL_EXT_discard_framebuffer",
                    "GL_EXT_multi_draw_arrays",
                    "GL_EXT_shader_texture_lod",
                    "GL_EXT_texture_format_BGRA8888",
                    "GL_IMG_multisampled_render_to_texture",
                    "GL_IMG_program_binary",
                    "GL_IMG_read_format",
                    "GL_IMG_shader_binary",
                    "GL_IMG_texture_compression_pvrtc",
                    "GL_IMG_texture_format_BGRA8888",
                    "GL_IMG_texture_npot",
                    "GL_IMG_vertex_array_object",
                    "GL_OES_EGL_image",
                    "GL_OES_EGL_image_external",
                    "GL_OES_blend_equation_separate",
                    "GL_OES_blend_func_separate",
                    "GL_OES_blend_subtract",
                    "GL_OES_byte_coordinates",
                    "GL_OES_compressed_ETC1_RGB8_texture",
                    "GL_OES_compressed_paletted_texture",
                    "GL_OES_depth24",
                    "GL_OES_depth_texture",
                    "GL_OES_draw_texture",
                    "GL_OES_egl_sync",
                    "GL_OES_element_index_uint",
                    "GL_OES_extended_matrix_palette",
                    "GL_OES_fixed_point",
                    "GL_OES_fragment_precision_high",
                    "GL_OES_framebuffer_object",
                    "GL_OES_get_program_binary",
                    "GL_OES_mapbuffer",
                    "GL_OES_matrix_get",
                    "GL_OES_matrix_palette",
                    "GL_OES_packed_depth_stencil",
                    "GL_OES_point_size_array",
                    "GL_OES_point_sprite",
                    "GL_OES_query_matrix",
                    "GL_OES_read_format",
                    "GL_OES_required_internalformat",
                    "GL_OES_rgb8_rgba8",
                    "GL_OES_single_precision",
                    "GL_OES_standard_derivatives",
                    "GL_OES_stencil8",
                    "GL_OES_stencil_wrap",
                    "GL_OES_texture_cube_map",
                    "GL_OES_texture_env_crossbar",
                    "GL_OES_texture_float",
                    "GL_OES_texture_half_float",
                    "GL_OES_texture_mirrored_repeat",
                    "GL_OES_vertex_array_object",
                    "GL_OES_vertex_half_float"])
deviceconfig.smallestScreenWidthDP = 320
#deviceconfig.deviceFeature.extend()
deviceconfig.unknown30 = 2

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
payload.otaCert.append('lIbs5KNFXmSDFVsGAYhR5r5I/ig=')
payload.serialNumber = functions.generateSerial()
payload.deviceConfiguration.CopyFrom(deviceconfig)
payload.macAddrType.append('wifi')
payload.fragment = 0
payload.userSerialNumber = 0
payload.droidguardResult = ''
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
with open('test_response', 'w') as result:
    result.write(r.text)
    result.close()
#print(r.text)
print(r.headers)
