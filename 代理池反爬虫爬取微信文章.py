
# coding: utf-8

# In[3]:


import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
base_url='https://weixin.sogou.com/weixin?'
headers={
    'Cookie':'SUV=00CD3A687B9E93695C49AB4FB8F32104; CXID=4AE711E74F73FD78436C9AB02BBB7256; SUID=AA14997B3965860A5C5575E600038557; sw_uuid=8415714725; sg_uuid=9950846157; ssuid=610394160; SNUID=BF0A2AEE272DA996CCCCB0BD28B917B0; ld=Oyllllllll2tYimYlllllVe0uiklllllek1Hulllll9lllllRylll5@@@@@@@@@@; ad=cyjDyZllll2tqggulllllVeubS7lllllWi6U$kllll9lllllRh7ll5@@@@@@@@@@; IPLOC=CN3310; ABTEST=4|1550284210|v1; weixinIndexVisited=1; sct=1; JSESSIONID=aaa6BticV_g9NhCjtJQIw',
    'Host':'weixin.sogou.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
proxy_pool_url='http://127.0.0.1:5000/get'
proxy=None
#max_count=5
def get_html(url):       #递归利用代理IP请求网页
    print('爬取网址为：',url)
#     print('爬取次数为：',count)
    global proxy
#     if count>=max_count:
#         print('请求太多次了')
#         return None
    try:
        if proxy:        #如果proxy为True
            proxies={'http':'http://'+proxy}
            response=requests.get(url,allow_redirects=False,headers=headers,proxies=proxies)   
        else:
            response=requests.get(url,allow_redirects=False,headers=headers)
            
        if response.status_code==200:       #如果请求返回码为200
            return response.text            
        if response.status_code==302:       #如果返回码为302
            print('get请求失败,错误码为302，请重新请求。')                
            proxy=get_proxy()         #调用get_proxy()函数，获得一个新的代理IP
            if proxy:                 #如果新的代理IP存在
                print('Using Proxy:',proxy)
                return get_html(url)          #递归调用自己
            else:                      #如果新的代理IP不存在
                print('获取Proxy失败,正在重新获取')
                proxy=get_proxy()
                return get_html(url)  
    except ConnectionError as e:
        print('错误次数:',e.args)
        proxy=get_proxy()
        return get_html(url)
def get_proxy():
    try:
        response=requests.get(proxy_pool_url)
        if response.status_code==200:
            return response.text
        return None
    except ConnectionError:
        return None
def get_index(keyword,page):    #传入搜索关键字和页码返回
    data={
        'query':keyword,
        'type':'2',
        'page':page
    }
    queries=urlencode(data)
    url=base_url+queries
    html=get_html(url)
    return html

def parse_index(html):
    doc=pq(html)
    items=doc('.news-box .news-list li .txt-box h3 a').items()
    print(items)
    for item in items:
        yield item.attr('href')
def main():
    keyword='风景'
    
    for page in range(1,10):
        html=get_index(keyword,page)
        if html:
            print(html)
            article_urls=parse_index(html)
            for article_url in article_urls:
                print(article_url)
if __name__=='__main__':
    main()
        

