爬取猫眼电影`Top100`的简单小爬虫，主要过程是：

1. 使用`request`库通过`get`请求获取到`top100`的`html`页面
2. 使用正则表达式`re`库解析出需要的内容
3. 将解析出的内容转换成`json`数据格式，并存储到`result.txt`中
4. 开启`python`多线程技术，以加快爬取速度
