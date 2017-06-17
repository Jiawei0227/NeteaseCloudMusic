# -*- coding:utf-8 -*-
import urllib2
import re
import DataBase
from bs4 import BeautifulSoup
import Logger
logger = Logger.Log()

class Song(object):
    def __init__(self,album):
        self.albumId = album
        self.url = "http://music.163.com/album?id=%d"%(int(album))
        self.sql = DataBase.Mysql()

    def pocess(self):
        request = urllib2.Request(self.url)
        res_data = urllib2.urlopen(request)
        soup = BeautifulSoup(res_data.read(),"lxml")
        songs = soup.find_all(name="a",attrs={"href":re.compile(r'/song\?id=\d+')})
        songList = []
        for song in songs:
            songId, name = re.findall(r'id=(.*)\">(.*)<',str(song),re.S)[0]
            data = {
                    "id": str(songId),
                    "name": name,
                    "album":self.albumId
                    }
            songList.append(data)

        return songList

def main():
    a = Song(3279543)
    a.pocess()

if __name__ == '__main__':
    main()
