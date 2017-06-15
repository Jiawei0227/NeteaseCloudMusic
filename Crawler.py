# -*- coding:utf-8 -*-
import EncryptUtil

def main():
    offset = 31
    requestUrl = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_483671599/"
    EncryptUtil.getComment(requestUrl,offset)

if __name__ == '__main__':
    main()
