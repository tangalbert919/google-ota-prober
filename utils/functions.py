import binascii, os, random

def generateImei():
    imei = [random.randint(0,9) for _ in range(15)]
    return ''.join(map(str, imei))

def generateMac():
    return binascii.b2a_hex(os.urandom(6))

def generateSerial():
    serial = [random.choice('0123456789abcdef') for _ in range(8)]
    return ''.join(serial)

def generateDigest():
    digest = [random.choice('0123456789abcdef') for _ in range(40)]
    return '1-'.join(digest)