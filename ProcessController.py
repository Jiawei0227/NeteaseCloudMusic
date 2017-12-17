# -*- coding:utf-8 -*-
import CrawlerSong
import CrawlerAlbum
import CrawlerComments
import json
import Logger
logger = Logger.Log()

class ProcessController(object):

    def __init__(self):
        pass

    def trigger(self,musicId,offset):
        isOk = False
        albumList = self.load()
        for album in albumList:
            if isOk:
                break

            if album["isCrawler"] == 1:
                continue
            for song in album["songs"]:
                if song["id"] == musicId:
                    if offset == "-1":
                        song["isCrawler"] = 1
                        for song in album["songs"]:
                            isCrawler = 1
                            if song["isCrawler"] == 0:
                                isCrawler = 0
                                break
                        album["isCrawler"] = isCrawler
                    else:
                        song["offset"] = offset
                    isOk = True
                    logger.critical("%s has fininsh with %s"%(str(musicId),str(offset)))
                    break

        self.store(albumList)

    def test(self):
        albumList = self.load()
        for album in albumList:
            album["isCrawler"] = 0
            for song in album["songs"]:
                song["isCrawler"] = 0
        self.store(albumList)

    def start(self):
        albumList = self.load()
        for album in albumList:
            if album["isCrawler"] == 1:
                continue
            for song in album["songs"]:
                if song["isCrawler"] == 1:
                    continue
                c = CrawlerComments.Crawler(song["id"],self)
                c.process(song["offset"])

    def initTaskSchedule(self):
        a = CrawlerAlbum.Album(2116)
        albumList = a.pocess()
        for album in albumList:
            album["isCrawler"] = 0
            s = CrawlerSong.Song(album["id"])
            songs = s.pocess()
            for ss in songs:
                ss["offset"] = 1
                ss["isCrawler"] = 0
            album["songs"] = songs
        self.store(albumList)


    def store(self,data):
        with open('TaskSchedule.json', 'w') as json_file:
            json_file.write(json.dumps(data))

    def load(self):
        with open('TaskSchedule.json') as json_file:
            data = json.load(json_file)
            return data



def main():
    p = ProcessController()
    p.start()


if __name__ == '__main__':
    main()
