# -*- coding: utf-8 -*-
import MySQLdb
import setting
import time
import Logger

logger = Logger.Log()


class Mysql:

    #获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

    #数据库初始化
    def __init__(self):
        try:
            self.db = MySQLdb.connect(
                    host=setting.MYSQL_HOST,
                    port = int(setting.MYSQL_PORT),
                    user=setting.MYSQL_USER,
                    passwd=setting.MYSQL_PASSWD,
                    db =setting.MYSQL_DBNAME,
                    charset="utf8mb4"
                    )
            self.cur = self.db.cursor()
        except MySQLdb.Error,e:
            logger.error("连接数据库错误",exc_info=True)

    #插入数据
    def insertData(self, table, my_dict):
         try:
             self.db.set_character_set('utf8mb4')
             cols = ', '.join(my_dict.keys())
             values = '"," '.join(my_dict.values())
             sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, '"'+values+'"')
             try:
                 result = self.cur.execute(sql)
                 insert_id = self.db.insert_id()
                 self.db.commit()
                 #判断是否执行成功
                 if result:
                     return insert_id
                 else:
                     return 0
             except MySQLdb.Error,e:
                 #发生错误时回滚
                 self.db.rollback()
                 #主键唯一，无法插入
                 if "key 'PRIMARY'" in e.args[1]:
                     logger.warning("数据已存在，未插入数据")
                 else:
                     logger.error("数据已存在，未插入数据",exc_info=True)
                 return -1
         except MySQLdb.Error,e:
             logger.error("数据库错误",exc_info=True)
             return -1

if __name__=='__main__':
    d = Mysql()
    commentData = {
        'id': '1',
        'user': '1',
        'content': '\xF0\x9F\x8E\xA4',
        'likeCount': '1'
    }
    d.insertData('comment',commentData)
