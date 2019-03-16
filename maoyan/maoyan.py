import requests
import re
import json
from multiprocessing import Pool
from requests.exceptions import RequestException

# 获取一个页面，其中一个页面有10个电影描述
def get_one_page(url):
    headers = {"User-Agent":
               "Mozilla/5.0 (Windows NT 10.0; WOW64) "
               "AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/72.0.3626.121 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 解析一个页面中的内容
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
    +'.*?>(.*?)</a>.*?star">\s+(.*?)\s+</p>.*?releasetime">(.*?)</p>'
    +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern, html)
    # print(items)
    for item in items:
        yield{
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time':  item[4].strip()[5:],
            'score': item[5] + item[6]
        }
# 将解析出的数据以json格式存到文件中
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')
        f.close()
# 主程序
def main(offset):
    url = "https://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
# 开启多线程技术，加快爬取速度
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])