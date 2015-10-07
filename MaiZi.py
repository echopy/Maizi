# coding: utf-8
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
'''

download 麦子学院 全部视频

开发环境  python 2.7

'''

idnexurls = []

if __name__ == '__main__':
    ''' Test '''
    i = 1
    j = 99
    while i <= j:
        try:
            url = 'http://www.maiziedu.com/course/list/?catagory=all&career=all&sort_by=&page=' + str(i)
            html = urllib2.urlopen(url).read().encode('gbk', 'ignore')
            '''
                <a title="C语言语法概述	" href="/course/qrsqd/2-810">
                    <p>
                        <img alt="C语言语法概述	" src="/uploads/course/2015/07/1.2C语言语法概述_lgZo42M.png"></p>
                    <div class="">
                        <p class="font14">C语言语法概述	</p><p class="color99">675人正在学习</p>
                    </div>
                </a>
            '''
            urls = re.findall('<li>\s*<a title="(.*?)"\s*href="(.*?)">', html, re.S)
            if i == 1:
                j = int(re.findall('共<span id="page-pane2">(.*?)</span>页，', html, re.S)[0])
            for url in urls:
                idnexurls.append((url[0],url[1]))
            i += 1
        except urllib2.HTTPError , e:
                break
    spdzs = []
    for url in idnexurls:
        try:
            print url[1]
            html = urllib2.urlopen('http://www.maiziedu.com/'+ url[1]).read().encode('gbk', 'ignore')
            spurls = re.findall('<li .*?>\s*<a href="(.*?)".*?lesson_id=\d*>(.*?)</a>', html, re.S)
            for spurl in spurls:
                if not re.search('\d', spurl[0], re.S):
                    spurls.append((url[1], ''))

            for spurl in spurls:
                    if not re.search('\d', spurl[0], re.S):
                        html = urllib2.urlopen('http://www.maiziedu.com/' + spurls[len(spurls)-1][0]).read().encode('gbk', 'ignore')
                        s = re.findall('<source src="(.*?)" type=\'video/mp4\'/>', html, re.S)
                        print s
                        spdzs.append((s, spurl[1]))
                        continue
                    if spurls[len(spurls)-1][0] == spurl[0]:
                        continue
                    html = urllib2.urlopen('http://www.maiziedu.com/' + spurl[0]).read().encode('gbk', 'ignore')
                    s = re.findall('<source src="(.*?)" type=\'video/mp4\'/>', html, re.S)
                    print s
                    spdzs.append((s, spurl[1]))

        except urllib2.HTTPError , e:
            break