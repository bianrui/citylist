#!/usr/bin/python
# -*-coding:utf-8-*-



from bs4 import BeautifulSoup
import urllib2
import sqlite3

archives_url = "http://static.weizhang8.cn/myjs/cityinfo_all.js?v=20161225"


def download(url):
    print url
    if url is None:
        return None
    print url

    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
    response = urllib2.urlopen(req)

    print "retu"
    if response.getcode() != 200:
        print 'url error'
        return None
    return response.read()


def parse(page_url, html_cont):

    print "page_url --  %s" % page_url
    # print "vvv%s" % html_cont
    if page_url is None or html_cont is None:
        print "vv0"
        return


    print html_cont
    print html_cont[2]

    sStr2 = '|'
    sStr1 = html_cont[html_cont.find("北京") + 1:]
    print sStr1
    print len(html_cont.split('|')[0].split(','))
    print len(html_cont.split('|')[10].split(','))
    print html_cont.split('|')[2]

    conn = sqlite3.connect("./data.db")
    conn.text_factory = str

    for item in html_cont.split('|'):
        element = item.split(',')

        if len(element)<31:
            continue
        Pinyin = ''
        if element[18].strip():
            Pinyin = element[18].strip()
        elif element[23].strip():
            Pinyin = element[23].strip()
        elif element[27].strip():
            Pinyin = element[27].strip()



        print (element[1],element[3],element[2],element[5],element[4],element[12],element[18])
        conn.execute("INSERT INTO cityData ( Province, Abbreviation, CityName, AreaCode, Code, TFF, Pinyin)"
                     " VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (element[1],element[3],element[2],element[5],element[4],element[12],Pinyin))



    conn.commit()
    conn.close()



    # conn = sqlite3.connect("./city.db")
    # print 'asdfasdfasfasdf'
    # print 'conn',conn
    #
    #
    # for item in res_data:
    #     res_dict = {}
    #     print "asdfadsfasd"
    #     summary_node = item.find_all('p',class_='MsoNormal')
    #     print summary_node
    #
    #     for li in summary_node:
    #         cityCode = li.find('span',lang="EN-US").get_text().strip()
    #         # print li
    #         citys = li.find_all('span', style="font-family: 宋体")
    #         if len(citys)>1:#获得城市
    #             cityName = citys[1].get_text().strip()
    #             print type(cityName)
    #             print type("市辖区")
    #             if cityName.encode('utf8') == "市辖区":
    #                 continue
    #             conn.execute("INSERT INTO cityTable ( cityCode, province, cityName) VALUES (?,?,?)",
    #                          (cityCode, "", cityName))
    #         else:#获得省份
    #             cityName = citys[0].get_text()
    #             print cityCode,"     ",cityName
    #             conn.execute("INSERT INTO cityTable ( cityCode, province, cityName) VALUES (?,?,?)", (cityCode, cityName, ""))
    #

    print 'Search over'




if __name__ == '__main__':
    html_cont = download(archives_url)
    parse(archives_url,html_cont)




