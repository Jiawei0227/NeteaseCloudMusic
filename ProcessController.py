# -*- coding:utf-8 -*-
import CrawlerSong
import CrawlerAlbum
import CrawlerComments

class ProcessController(object):

    def __init__(self):
        pass

    def test(self):
        a = CrawlerAlbum.Album(2116)
        albumList = a.pocess()
        for album in albumList:
            s = CrawlerSong.Song(album["id"])
            songList = s.pocess()
            for song in songList:
                c = CrawlerComments.Crawler(song["id"])
                c.start()


def main():
    p = ProcessController()
    p.test()

if __name__ == '__main__':
    main()
