# -*- coding:utf-8 -*-
import os
import json
import base64
import urllib2
import urllib
from Crypto.Cipher import AES

modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'

def createSecretKey(size):
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:size]

def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext

def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(text.encode('hex'), 16)**int(pubKey, 16)%int(modulus, 16)
    return format(rs, 'x').zfill(256)


def getComment(requestUrl, offset):
    username = ""
    password = ""
    text = {
        'username': username,
        'password': password,
        'rememberLogin': 'true',
        'offset': offset
    }
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }

    data_urlencode = urllib.urlencode(data)
    req = urllib2.Request(url = requestUrl,data =data_urlencode)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    print res
    file = open("comment","a")

    for comment in json.loads(res)["comments"]:
        file.write(comment['content'].encode('utf-8'))
        file.write('\n')
    file.write('--------------------------' + str(offset)+'------------------------')

    file.close()
