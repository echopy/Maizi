# coding: utf-8

import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class VideoDB:
    def __init__(self):
        # 初始化Mysql连接请求
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'cidao1!'
        self.db = 'maizi'
        self.charset = 'utf8'
        # 数据库游标
        self.conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'cidao1!',db = 'maizi',charset = 'gbk',)
        self.cursor = self.conn.cursor()


    def Create(self):
        """
        创建数videoInfo表
        """
        sql = """
            create table videoInfo(
              id int primary key auto_increment,
              filename varchar(256),
              indexurl varchar(256),
              title varchar(256),
              videourl varchar(256)
            )
            """

        self.cursor.execute(sql)
        self.cursor.commit()

    def insert(self, title, url, videotitle, video):
        """
        向数据库插入数据
        """
        print title, url, videotitle, video
        sql = 'insert into videoinfo (filename ,url, title,video) values (\'%s\', \'%s\', \'%s\', \'%s\')' % (title, url, videotitle, video,)
        self.cursor.execute(sql)
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
