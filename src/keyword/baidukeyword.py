__author__ = 'Administrator'

import os
import pymysql
import xlrd

class BaiduKeywordTool():

    keyword_map = {}

    def init_keywords_map(self):
        try:
            conn = pymysql.connect(host="localhost", user="root", passwd="admin", db="seodb", port=3306, charset="utf8")
            cur = conn.cursor()
            cur.execute("select keyword,computer_daily_search from seo_keyword")
            rows = cur.fetchall()
            for row in rows:
                self.keyword_map.setdefault(row[0], row[1])

            cur.close()
            conn.close()
        except Exception as e:
            print(e)

    def export_keyword_dict(self, file_name):
        try:
            output_file = open(file_name, 'w', encoding="utf8")
            conn = pymysql.connect(host="localhost", user="root", passwd="admin", db="seodb", port=3306, charset="utf8")
            cur = conn.cursor()
            cur.execute("select keyword,daily_search_total,keyword_length from seo_keyword "
                        "where keyword_length<=6 order by keyword_length asc")
            rows = cur.fetchall()
            for row in rows:
                if(" " in row[0]):
                    continue
                output_file.write(row[0] + " " + str(row[2]) + " n\n")

            cur.close()
            conn.close()

            output_file.close()
        except Exception as e:
            print(e)

    def import_keywords(self, seed_word, file, sheet_name):
        print("<import_keywords> seed_word " + seed_word + ", file: " + file)
        wb = xlrd.open_workbook(file)
        sheet = wb.sheet_by_name(sheet_name)
        keywords = []
        rows_count = sheet.nrows
        for i in range(1, rows_count):
            keyword = sheet.cell(i, 0).value
            if(None == self.keyword_map.get(keyword)):
                self.keyword_map.setdefault(keyword, 1)
            else:
                continue

            show_reason = sheet.cell(i, 1).value
            daily_search_total = sheet.cell(i, 2).value
            mobile_daily_search = sheet.cell(i, 3).value
            computer_daily_search = sheet.cell(i, 4).value
            suggest_bid = sheet.cell(i, 5).value
            competition = sheet.cell(i, 6).value

            keywords.append((keyword, seed_word, show_reason, int(daily_search_total), int(mobile_daily_search),
                             int(computer_daily_search), float(suggest_bid), int(competition), len(keyword)))
        return keywords

    def save_keywords(self, seed_word, keywords):
        print("<save_keywords> seed_word " + seed_word + ", keywords count: " + str(len(keywords)))
        try:
            conn = pymysql.connect(host="localhost", user="root", passwd="admin", db="seodb", port=3306, charset="utf8")
            cur = conn.cursor()

            sql = """insert into seo_keyword(keyword,seedword,
            show_reason,daily_search_total,mobile_daily_search,
            computer_daily_search,suggest_bid,competition,keyword_length,date_created)
             values(%s, %s, %s, %s, %s, %s, %s, %s, %s, now())"""

            for word_row in keywords:
                print(word_row)
                cur.execute(sql, word_row)

            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(e)

    def batch_import_keywords(self, dir):
        print("<batch_import_keywords> dir " + dir)
        if os.path.isdir(dir):
            for file in os.listdir(dir):
                if file.endswith('xls'):
                    print(file)
                    seed_word = file.strip(".xls")
                    xls_file = dir + os.sep + file
                    keyword_list = self.import_keywords(seed_word, xls_file, "Sheet0")
                    self.save_keywords(seed_word, keyword_list)

            for file in os.listdir(dir):
                if not file.endswith('xls'):
                    print(file)
                    if(os.path.isdir(dir + os.sep + file)):
                        self.batch_import_keywords(dir + os.sep + file)

keyword_tool = BaiduKeywordTool()
keyword_tool.export_keyword_dict("D:\dev\python\seo-tool\conf\keyword_dict.txt")

# keyword_tool.init_keywords_map()
# keyword_tool.batch_import_keywords("D:\dev\python\seo-tool\conf\keywords")

# keyword_list = keyword_tool.import_keywords("大数据分析", "D:\dev\python\seo-tool\conf\大数据分析.xls", "Sheet0")
# keyword_tool.save_keywords("大数据分析", keyword_list)
