# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests, sys

"""
类说明:下载《笔趣看》网小说《一念永恒》
1、通过小说目录的URL，获取整本小说所有的章节URL
2、每一章节分别爬取章节内容
3、每一章节分别写入文件中
4、主函数循环调用2、3的方法，最终将所有章节写入文件
Parameters:
	无
Returns:
	无
Modify:
	2019-05-06
"""
class Downloader(object):

	def __init__(self):
		self.server = 'http://www.biqukan.com/'
		self.target = 'http://www.biqukan.com/1_1094/'
		self.names = []			#存放章节名
		self.urls = []			#存放章节链接
		self.nums = 0			#章节数

	"""
	函数说明:获取下载链接
	Parameters:
		无
	Returns:
		无
	Modify:
		2019-05-06
	"""
	def get_download_url(self):
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
		}
		response = requests.get(url = self.target, headers=headers)
		html = response.text
		div_bf = BeautifulSoup(html, 'lxml')
		# print(div_bf)
		div = div_bf.find_all('div', class_ = 'listmain')
		# print(div)
		a_bf = BeautifulSoup(str(div[0]), 'lxml')
		a_tag = a_bf.find_all('a')
		self.nums = len(a_tag[16:20])								#剔除不必要的章节，并统计章节数
		for each in a_tag[16:20]:
			self.names.append(each.string)
			self.urls.append(self.server + each.get('href'))

	"""
	函数说明:获取章节内容
	Parameters:
		target - 下载链接(string)
	Returns:
		texts - 章节内容(string)
	Modify:
		2019-05-06
	"""
	def get_contents(self, each_chapter_url):
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
		}
		response = requests.get(url = each_chapter_url, headers=headers)
		html_bytes = response.content.replace(b'\r\n', b'\r').replace(b'\r', b'\r\n')
		# print(html_bytes)
		html = html_bytes.decode('gbk')
		# print(type(html))
		# print(html)
		bf = BeautifulSoup(html,'lxml')
		texts = bf.find_all('div', class_ = 'showtxt')
		# print(type(texts[0].text))
		texts = texts[0].text.replace('\xa0'*8,'')
		# print(texts)
		return texts

	"""
	函数说明:将爬取的文章内容写入文件
	Parameters:
		name - 章节名称(string)
		path - 当前路径下,小说保存名称(string)
		text - 章节内容(string)
	Returns:
		无
	Modify:
		2019-05-06
	"""
	def writer(self, name, path, text):
		# write_flag = True
		with open(path, 'a', encoding='utf-8') as f:
			f.write(name + '\r\n')
			f.writelines(text)
			f.write('\r\n')

# test
# d = Downloader()
# url = 'https://www.biqukan.com/1_1094/5403177.html'
# d.get_download_url()



if __name__ == "__main__":
	dl = Downloader()
	dl.get_download_url()
	print('《一念永恒》开始下载：')
	for i in range(dl.nums):
		dl.writer(dl.names[i], '一念永恒.txt', dl.get_contents(dl.urls[i]))
		print("  已下载:%.3f%%" %  float(i/dl.nums*100) + '\r')
		# sys.stdout.write("  已下载:%.3f%%" %  float(i/dl.nums*100) + '\r')
		# sys.stdout.flush()
	print('《一念永恒》下载完成')
