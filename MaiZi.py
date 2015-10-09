#coding: utf-8
'''
当前版本: 0.1
'''
import re
import urllib2
import sys
import os
import urllib
import Mysql
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')

class MaiZi:
    def __init__(self):
        # 麦子学院 视频初始地址
        self.indexurl = 'http://www.maiziedu.com/course/list/?catagory=all&career=all&sort_by=&page='
        # 视频列表
        self.videolist = []
        # 视频索引地址
        self.videoIndexUrls = []
        # headers
        self.headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2522.0 Safari/537.36'}
        # 全部视频urls
        self.AllVideoUrls = []
        self.mysql = Mysql.VideoDB()

    def GetHtml(self, url):
        """
        获取页面源码
        """
        request = urllib2.Request(url, headers=self.headers)
        return urllib2.urlopen(request).read().encode('gbk', 'ignore')

    def Allurls(self, html):
        """
        获取当前页面urls
        """
        urlsinfo = re.findall('<li>\s*<a title="(.*?)"\s*href="(.*?)">', html, re.S)
        for urlinfo in urlsinfo:
            self.videoIndexUrls.append(list(urlinfo))

    def GetAllVideoUrls(self, html):
        """
        获取当前html内的所有视频Url
        """
        urls = re.findall('<li .*?>\s*<a href="(.*?)".*?lesson_id=\d*>(.*?)</a>', html, re.S)
        for url in urls:
            self.AllVideoUrls.append(list(url))

    def GetVideoList(self, html):
        """
        获取视频地址
        """
        return re.findall('<source src="(.*?)" type=\'video/mp4\'/>', html, re.S)

    # 输出下载进度
    def Schedule(self, downloadSize, dataSize, remotelyFileSize):
        '''
        downloadSize:已经下载的数据块
        dataSize:数据块的大小
        remotelyFileSize:远程文件的大小
       '''
        per = 100.0 * downloadSize * dataSize / remotelyFileSize
        if per > 100:
            per = 100

        print u'当前下载进度:%.2f%%\r' % per,

    def run(self):
        # 获取最大页数页数
        maxPage = int(re.findall('<span id="page-pane2">(.*?)</span>', self.GetHtml(self.indexurl), re.S)[0])
        page = 0
        while page <= maxPage:
            url = self.indexurl + str(page)
            self.Allurls(self.GetHtml(url))
            for videoIndexurl in self.videoIndexUrls:
                title = videoIndexurl[0]
                url = 'http://www.maiziedu.com/' + videoIndexurl[1]
                print title,url
                self.GetAllVideoUrls(self.GetHtml(url))
                # os.mkdir(title)
                for VideoUrlin in self.AllVideoUrls:
                    title = VideoUrlin[1]
                    if not re.search('\d', VideoUrlin[0]):
                        url = 'http://www.maiziedu.com/' + videoIndexurl[1]
                    else:
                        url = 'http://www.maiziedu.com/' + VideoUrlin[0]
                    title = title.replace('&nbsp;','').strip()
                    video = self.GetVideoList(self.GetHtml(url))[0]

                    self.mysql.insert(title, url, videoIndexurl[0],video)

                    # filename = os.path.join(videoIndexurl[0].strip(), title + '.mp4')
                    # urllib.urlretrieve(video, filename, self.Schedule)
            page += 1

if __name__ == '__main__':
    maizi = MaiZi()
    maizi.run()