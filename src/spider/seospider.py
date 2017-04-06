#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
# from bs4 import
import xlrd
import xlwt

class SeoSpider():

    def analyse(self, domain, url, params):
        """分析页面"""
        result = {'title': '', 'keywords': '', 'description': ''}
        try:
            header = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                 "Accept": "text/plain"}
            data = urllib.parse.urlencode(params).encode(encoding='UTF8')
            req = urllib.request.Request(url, data, headers=header)
            response = urllib.request.urlopen(req)
            content = response.read()

            soup = BeautifulSoup(content.decode('utf8'))
            result['title'] = soup.title.string

            # 分析meta标签获取页面keywords和description
            meta_list = soup.find_all('meta')
            for tag in meta_list:
                if 'name' in tag.attrs:
                    if tag.attrs['name'] == "keywords":
                        result['keywords'] = tag.attrs['content']
                    elif tag.attrs['name'] == "description":
                        result['description'] = tag.attrs['content']

            # 分析链接
            link_list = soup.find_all('a')
            # for tag in link_list:
            #     # print(tag.get_text())
            #     if 'href' in tag.attrs:
            #         print("href=" + tag.attrs['href'])

                # print("text=" + tag.string)
        except Exception as e:
            print(e)
        return result

    def read_excel(self, file, sheet_name):
        wb = xlrd.open_workbook(file)
        sheet = wb.sheet_by_name(sheet_name)
        urls = []
        cols_count = sheet.ncols
        rows_count = sheet.nrows
        for i in range(1, rows_count):
            # row_data = []
            # for j in range(0, cols_count):
            #     row_data[j] = sheet.cell(i, j).value
            url = sheet.cell(i, 8).value
            urls.append(url)
            # print(url)
            # protocol, rest = urllib.parse.splittype(url)
            # print(rest)
            # domain, rest = urllib.parse.splithost(rest)
            # print(rest)
            # print(protocol)
            # print(domain)
        return urls

     # 输出excel
    def write_excel(self, file, sheet_name, titles, datas):
        # 创建工作簿
        wb = xlwt.Workbook()

        # 创建sheet
        sheet = wb.add_sheet(sheet_name, cell_overwrite_ok=True)

        # 初始化Title样式
        title_style = xlwt.XFStyle()
        title_font = xlwt.Font()
        #title_font.name = 'Times New Roman'
        title_font.bold = True
        title_font.color_index = 4
        title_font.height = 220

        # title_borders= xlwt.Borders()
        # title_borders.left= 6
        # title_borders.right= 6
        # title_borders.top= 6
        # title_borders.bottom= 6

        title_style.font = title_font
        # style.borders = borders

        # 初始化Cell样式
        cell_style = xlwt.XFStyle()
        cell_font = xlwt.Font()
        #cell_font.name = 'Times New Roman'
        cell_font.bold = False
        cell_font.color_index = 4
        cell_font.height = 200
        cell_style.font = cell_font

        # 生成标题行
        for i in range(0, len(titles)):
            sheet.write(0, i, titles[i], title_style)

        # 生成数据Cell
        for i in range(0, len(datas)):
            data = datas[i]
            for j in range(0, len(titles)):
                sheet.write(i + 1, j, data[j], cell_style)

        wb.save(file)

spider = SeoSpider()
urls = spider.read_excel("D:\dev\python\seo-tool\conf\IBM Landing Page.xls", "cloud")

titles = [u'序号', u'URL', u'Page Title', u'Meta Keywords', u'Meta Description', u'关键词', u'链接数量']
dataList = []
for i in range(0, len(urls)):
    url = urls[i]
    print(url)
    protocol, rest = urllib.parse.splittype(url)
    domain, rest = urllib.parse.splithost(rest)
    result = spider.analyse(domain, url, {})
    data = []
    data.insert(0, i)
    data.insert(1, url)
    data.insert(2, result['title'])
    data.insert(3, result['keywords'])
    data.insert(4, result['description'])
    data.insert(5, '')
    data.insert(6, '')
    dataList.append(data)

spider.write_excel('D:\dev\python\seo-tool\conf\demo.xls', "Cloud", titles, dataList)

# result = spider.analyse("www.ibm.com", "http://www-31.ibm.com/ibm/cn/cognitive/outthink/", {})
# # result = spider.analyse("www.ibm.com", "https://www.ibm.com/analytics/cn/zh/technology/", {})
# # result = spider.analyse("www.ibm.com", "https://www.ibm.com/cn-zh/", {})
# print("title: " + result['title'])
# print("keywords: " + result['keywords'])
# print("description: " + result['description'])