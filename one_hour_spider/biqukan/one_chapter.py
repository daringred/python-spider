from urllib import request
from bs4 import BeautifulSoup

if __name__ == "__main__":
    download_url = 'http://www.biqukan.com/1_1094/5403177.html'
    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    download_req = request.Request(url = download_url, headers = head)
    download_response = request.urlopen(download_req)
    # print(type(download_response))
    # print(type(download_response.read()))
    # print(download_response.read())
    download_html = download_response.read().replace(b'\r\n', b'\r').replace(b'\r', b'\r\n').decode('gbk','ignore')
    # print(type(download_html))
    # print(download_html)
    soup_texts = BeautifulSoup(download_html, 'lxml')
    # print(type(soup_texts))
    texts = soup_texts.find_all(id = 'content', class_ = 'showtxt')
    # print(type(texts))
    # print(texts)
    # print(str(texts))
    soup_text = BeautifulSoup(str(texts), 'lxml')
    # print(soup_text.div.text)
    # 将\xa0无法解码的字符删除
    print(soup_text.div.text.replace('\xa0',''))