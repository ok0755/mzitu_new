#coding=utf-8
import requests
import os
from time import sleep
from lxml import etree
import gevent
from gevent import monkey,pool
monkey.patch_all()

def pages(start,end):
    th = []
    for i in range(start,end):
        url="http://www.mzitu.com/page/{}".format(i)
        th.append(url)
    return th

def detail_page(url):
    sleep(1)
    headers={'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh - CN, zh;q = 0.9',
        'Cache - Control': 'max - age = 0',
        'Host': 'www.mzitu.com',
        'Upgrade - Insecure - Requests': '1',
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 66.0.3359.117 Safari / 537.36'}
    html = requests.get(url, headers=headers)
    selector=html.text
    html.close()
    selec = etree.HTML(selector)
    for ur in selec.xpath('//ul[@id="pins"]/li/a/@href'):
        yield ur

def getPiclink(url):
    headers={'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh - CN, zh;q = 0.9',
        'Cache - Control': 'max - age = 0',
        'Host': 'www.mzitu.com',
        'Upgrade - Insecure - Requests': '1',
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 66.0.3359.117 Safari / 537.36'}
    html = requests.get(url,headers=headers)
    text = html.text
    html.close()
    sel = etree.HTML(text)
    ## 图片总数
    total = sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    return url,total

def wait_down_pic(url,total):
    pic = []
    headers={'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh - CN, zh;q = 0.9',
        'Cache - Control': 'max - age = 0',
        'Host': 'www.mzitu.com',
        'Upgrade - Insecure - Requests': '1',
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 66.0.3359.117 Safari / 537.36',
        'referer': url}
    pic = requests.get(url,headers=headers)
    html = pic.text
    sele = etree.HTML(html)
    pic.close()
    jpglink = sele.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
    for t in range(1,int(total)+1):
        link = '{}{}{}'.format(jpglink[:-6],str(t).zfill(2),'.jpg')
        yield '{}/{}'.format(url,t),link
    ##yield jpglink

def down(url,pic_url):
    print pic_url
    headers={'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'referer': url}

    html = requests.get(pic_url,headers=headers)
    text = html.content
    html.close()
    filename = os.path.split(pic_url)[1]
    with open(filename,'wb+') as jpg:
        jpg.write(text)

start = input('Start of page:')
end = input('End of page:')
p = pages(start,end)
geventpool = pool.Pool(20)
for page in p:
    print u'正在下载....',page
    d = detail_page(page)
    for dd in d:
        urllists = getPiclink(dd)
        pics = wait_down_pic(urllists[0],urllists[1])
        th = []
        for pic in pics:
            th.append(gevent.spawn(down,pic[0],pic[1]))
        gevent.joinall(th,timeout=5)
            ##geventpool.spawn(down,pic[0],pic[1])
        ##geventpool.join()
'''
def pages(start,end):
    th = []
    for i in range(start,end):
        url="http://www.mzitu.com/page/{}".format(i)
        th.append(url)
    return th

def detail_page(url):
    sleep(1)
    headers={'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh - CN, zh;q = 0.9',
        'Cache - Control': 'max - age = 0',
        'Host': 'www.mzitu.com',
        'Upgrade - Insecure - Requests': '1',
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 66.0.3359.117 Safari / 537.36'}
    html = requests.get(url, headers=headers)
    selector=html.text
    html.close()
    selec = etree.HTML(selector)
    for ur in selec.xpath('//ul[@id="pins"]/li/a/@href'):
        yield ur

def getPiclink(url):
    th = []
    headers={'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh - CN, zh;q = 0.9',
        'Cache - Control': 'max - age = 0',
        'Host': 'www.mzitu.com',
        'Upgrade - Insecure - Requests': '1',
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 66.0.3359.117 Safari / 537.36'}
    html = requests.get(url,headers=headers)
    text = html.text
    html.close()
    sel = etree.HTML(text)
    ## 图片总数
    total = sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    for i in range(int(total)):
        link = '{}/{}'.format(url, i+1)
        th.append(link)
    return th

def wait_down_pic(url):
    pic = []
    headers={'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh - CN, zh;q = 0.9',
        'Cache - Control': 'max - age = 0',
        'Host': 'www.mzitu.com',
        'Upgrade - Insecure - Requests': '1',
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 66.0.3359.117 Safari / 537.36',
        'referer': url}
    pic = requests.get(url,headers=headers)
    html = pic.text
    sele = etree.HTML(html)
    pic.close()
    jpglink = sele.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
    yield jpglink

def down(url,pic_url):
    print url
    headers={'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'referer': url}

    html = requests.get(pic_url,headers=headers)
    text = html.content
    html.close()
    filename = os.path.split(pic_url)[1]
    with open(r'd:\mzitu\{}'.format(filename),'wb+') as jpg:
        jpg.write(text)

start = input('Start of page:')
end = input('End of page:')
p = pages(start,end)
geventpool = pool.Pool(15)
for page in p:
    d = detail_page(page)
    for dd in d:
        urllists = getPiclink(dd)
        for u in urllists:
            pics = wait_down_pic(u)
            th = []
            for pic_url in pics:
                th.append(gevent.spawn(down,u,pic_url))
            gevent.joinall(th,timeout=4)
'''