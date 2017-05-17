#!/usr/bin/python
# -*-coding:utf-8-*-



from bs4 import BeautifulSoup
import urllib2
import sqlite3

archives_url = "http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/201703/t20170310_1471429.html"


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

    # print "BeautifulSoup %s" % html_cont
    soup = BeautifulSoup(html_cont, "html.parser", from_encoding="utf-8")

    res_data = soup.find_all('div',class_='TRS_PreAppend')
    print res_data

    conn = sqlite3.connect("./city.db")
    print 'asdfasdfasfasdf'
    print 'conn',conn


    for item in res_data:
        res_dict = {}
        print "asdfadsfasd"
        summary_node = item.find_all('p',class_='MsoNormal')
        print summary_node

        for li in summary_node:
            cityCode = li.find('span',lang="EN-US").get_text().strip()
            # print li
            citys = li.find_all('span', style="font-family: 宋体")
            if len(citys)>1:#获得城市
                cityName = citys[1].get_text().strip()
                print type(cityName)
                print type("市辖区")
                if cityName.encode('utf8') == "市辖区":
                    continue
                conn.execute("INSERT INTO cityTable ( cityCode, province, cityName) VALUES (?,?,?)",
                             (cityCode, "", cityName))
            else:#获得省份
                cityName = citys[0].get_text()
                print cityCode,"     ",cityName
                conn.execute("INSERT INTO cityTable ( cityCode, province, cityName) VALUES (?,?,?)", (cityCode, cityName, ""))

    conn.commit()
    conn.close()
    print 'Search over'




if __name__ == '__main__':
    html_cont = download(archives_url)
    parse(archives_url, html_cont)


