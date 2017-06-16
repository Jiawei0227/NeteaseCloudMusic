# -*- coding:utf-8 -*-
import EncryptUtil
import json
import urllib2
import urllib
import time
import DataBase
import Logger

logger = Logger.Log()

class Crawler(object):

    def __init__(self,id):
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'
        pubKey = '010001'
        self.secKey = EncryptUtil.createSecretKey(16)
        self.encSecKey = EncryptUtil.rsaEncrypt(self.secKey, pubKey, modulus)
        self.mysql = DataBase.Mysql()
        self.musicId = id
        self.requestUrl = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%d/"%id

    def getComment(self, requestUrl, offset):
        username = ""
        password = ""
        text = {
            'username': username,
            'password': password,
            'rememberLogin': 'true',
            'offset': offset
        }
        text = json.dumps(text)
        encText = EncryptUtil.aesEncrypt(EncryptUtil.aesEncrypt(text, self.nonce), self.secKey)
        data = {
            'params': encText,
            'encSecKey': self.encSecKey
        }

        data_urlencode = urllib.urlencode(data)
        req = urllib2.Request(url = requestUrl,data =data_urlencode)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        jsonData = json.loads(res)
        self.databaseSave(jsonData)
        return int(jsonData["total"])

    def databaseSave(self ,jsonData):
        for comment in jsonData["comments"]:
            commentData = {
                'id': str(comment["commentId"]),
                'user': str(comment["user"]["userId"]),
                'content': comment["content"].encode('utf-8'),
                'likeCount': str(comment["likedCount"]),
                'commentTime': str(EncryptUtil.timeStamp(comment["time"])),
                'musicId': str(self.musicId)
            }
            if not comment["beReplied"] == []:
                commentData["reComment"] = str(comment["beReplied"][0]["user"]["userId"])

            if self.mysql.insertData("comment",commentData) >= 0:
                logger.info("Comment %s Saved."%commentData["id"])

            userData = {
                'id': str(comment["user"]["userId"]),
                'username': comment["user"]["nickname"].encode('utf-8'),
                'avatarUrl': comment["user"]["avatarUrl"].encode('utf-8')
            }
            if self.mysql.insertData("user",userData) >= 0:
                logger.info("User %s Saved."%userData["id"])

    def start(self):
        self.process(1)

    def process(self, offset):
        off = offset
        total = self.getComment(self.requestUrl,off)
        while off<total:
             off += 10
             self.getComment(self.requestUrl,off)

def main():
    c = Crawler(66842)
    c.start()

if __name__ == '__main__':
    main()
