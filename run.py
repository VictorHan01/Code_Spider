from spider import CodeSpider

url = 'http://code.tarena.com.cn/AIDCode/aid1907/'
auth = ('tarenacode', 'code_2013')
directory = 'E:/Python视频/测试/'

code_spider = CodeSpider(url,auth,directory)
code_spider.main()
