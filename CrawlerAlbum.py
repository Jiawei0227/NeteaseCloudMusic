# -*- coding:utf-8 -*-
import urllib2
import re
import DataBase
from bs4 import BeautifulSoup

logger = Logger.Log()

class Album(object):
    def __init__(self,artist):
        self.artistId = artist
        self.url = "https://music.163.com/artist/album?id=%d&limit=%d"%(artist,200)
        self.sql = DataBase.Mysql()

    def pocess(self):
        request = urllib2.Request(self.url)
        res_data = urllib2.urlopen(request)
        soup = BeautifulSoup(res_data.read(),"lxml")
        titles = soup.find_all(name="p",attrs={"class":"dec dec-1 f-thide2 f-pre"})
        ids = soup.find_all(name="a",attrs={"class":"tit s-fc0"})
        for a in ids:
            albumId,name = re.findall(r'id=(.*)\">(.*)<', str(a), re.M)[0]
            data = {
                "id":str(albumId),
                "name":name,
                "musicId":str(self.artistId)
                    }
            if sql.insertData("album",data) >= 0:
                logger.info("album %d : %s insert success"%(albumId,name))


def main():
    a = Album(2116)
    a.pocess()

if __name__ == '__main__':
    main()
