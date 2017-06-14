__author__ = 'Administrator'

import time
import pymysql
import xlrd

class PageVisitsTool():

    def import_page_visits(self, category, file, sheet_name, date):
        print("<import_page_visits> category: " + category + ", date: " + date + ", file: " + file)
        wb = xlrd.open_workbook(file)
        sheet = wb.sheet_by_name(sheet_name)
        page_visits_list = []
        rows_count = sheet.nrows
        for i in range(1, rows_count):
            page_date = sheet.cell(i, 0).value
            date_data = xlrd.xldate_as_tuple(page_date, 0)
            year = date_data[0]
            month = date_data[1]
            day = date_data[2]
            page_date = str(year) + "/" + str(month) + "/" + str(day)
            poe_source = sheet.cell(i, 8).value
            if date == page_date and"Organic Search" == poe_source:
                quarter = sheet.cell(i, 1).value
                qw = sheet.cell(i, 2).value

                peferrer_detail = sheet.cell(i, 9).value
                entry_detail = sheet.cell(i, 10).value
                visits = sheet.cell(i, 11).value
                visits_country = sheet.cell(i, 18).value
                entry_page = sheet.cell(i, 22).value
                traffic_source = sheet.cell(i, 36).value

                page_visits_list.append((category, page_date, year, month, day, quarter, qw,
                                         poe_source, peferrer_detail, entry_detail, int(visits), visits_country,
                                         entry_page, traffic_source))

        self.save_page_visits(category, page_visits_list)

        return page_visits_list

    def import_month_page_visits(self, category, table_name, file, sheet_name, import_month):
        print("<import_month_page_visits> category: " + category + ", import_month: " + import_month + ", file: " + file)
        wb = xlrd.open_workbook(file)
        sheet = wb.sheet_by_name(sheet_name)
        page_visits_list = []
        rows_count = sheet.nrows
        for i in range(1, rows_count):
            poe_source = sheet.cell(i, 8).value
            if import_month == sheet.cell(i, 3).value and "Organic Search" == poe_source:
                date = sheet.cell(i, 0).value
                date_data = xlrd.xldate_as_tuple(date, 0)
                year = date_data[0]
                month = date_data[1]
                day = date_data[2]
                quarter = sheet.cell(i, 1).value
                qw = sheet.cell(i, 2).value

                peferrer_detail = sheet.cell(i, 9).value
                entry_detail = sheet.cell(i, 10).value
                visits = sheet.cell(i, 11).value
                visitor_country = sheet.cell(i, 18).value
                entry_page = sheet.cell(i, 22).value
                traffic_source = sheet.cell(i, 36).value

                page_visits_list.append((category, date, int(year), int(month), int(day), quarter, qw,
                                         poe_source, peferrer_detail, entry_detail, int(visits), visitor_country,
                                         entry_page, traffic_source))

        self.save_page_visits(category, table_name, page_visits_list)

        return page_visits_list

    def save_page_visits(self, category, table_name, page_visits_list):
        print("<save_page_visits> category " + category + ", page_visits_list count: " + str(len(page_visits_list)))
        try:
            conn = pymysql.connect(host="localhost", user="root", passwd="admin", db="seodb", port=3306, charset="utf8")
            cur = conn.cursor()

            sql = "insert into " + table_name + "(category,date,year,month,day,quarter,qw,poe_source,peferrer_detail," \
                                                "entry_detail,visits,visitor_country,entry_page,traffic_source) " \
                                                "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            for row in page_visits_list:
                print(row[9])
                cur.execute(sql, row)

            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(e)

    def page_visits_report(self, category, table_name, urls, file_name):
        print("<page_visits_report> category: " + category, ", table_name: " + table_name + ", urls count: " + str(len(urls)))
        try:
            output_file = open(file_name, 'w', encoding="utf8")
            conn = pymysql.connect(host="localhost", user="root", passwd="admin", db="seodb", port=3306, charset="utf8")
            cur = conn.cursor()

            for url in urls:
                print("<page_visits_report> category: " + category + ", url: " + url)
                cur.execute("SELECT SUM(visits) from " + table_name + " where `year`=2017 and `month`=4 and (`day` >= 1 and `day` <=15) and entry_detail like '%" + url + "'")
                row = cur.fetchone()
                count2 = row[0]

                cur.execute("SELECT SUM(visits) from " + table_name + " where `year`=2017 and `month`=4 and (`day` >= 16 and `day` <=30) and entry_detail like '%" + url + "'")
                row = cur.fetchone()
                count3 = row[0]

                cur.execute("SELECT SUM(visits) from " + table_name + " where `year`=2017 and `month`=5 and (`day` >= 1 and `day` <=15) and entry_detail like '%" + url + "'")
                row = cur.fetchone()
                count4 = row[0]

                cur.execute("SELECT SUM(visits) from " + table_name + " where `year`=2017 and `month`=5 and (`day` >= 16 and `day` <=31) and entry_detail like '%" + url + "'")
                row = cur.fetchone()
                count5 = row[0]

                cur.execute("SELECT SUM(visits) from " + table_name + " where `year`=2017 and `month`=6 and (`day` >= 1 and `day` <=15) and entry_detail like '%" + url + "'")
                row = cur.fetchone()
                count6 = row[0]

                cur.execute("SELECT SUM(visits) from " + table_name + " where `year`=2017 and `month`=6 and (`day` >= 16 and `day` <=31) and entry_detail like '%" + url + "'")
                row = cur.fetchone()
                count7 = row[0]

                cur.execute("SELECT SUM(visits) from " + table_name + " where `quarter`='Q1' and entry_detail like '%" + url + "'")
                row = cur.fetchone()
                count1 = row[0]
                print(count1)

                cur.execute("SELECT SUM(visits) from " + table_name + " where `quarter`='Q2' and entry_detail like '%" + url + "'")
                row = cur.fetchone()
                count8 = row[0]

                output_file.write(url + "," + str(count1) + "," + str(count2) + "," + str(count3)
                                  + "," + str(count4) + "," + str(count5) + "," + str(count6)
                                  + "," + str(count7) + "," + str(count8) + "\n")

            cur.close()
            conn.close()

            output_file.close()
        except Exception as e:
            print(e)

page_visits_tool = PageVisitsTool()
# page_visits_tool.import_month_page_visits("Analytics", "seo_page_visits", "D:\dev\python\seo-tool\conf\GCG_Analytics_2017 YTD_20170.xlsx", "sourcedetail", "Jan")
# page_visits_tool.import_month_page_visits("Analytics", "seo_page_visits", "D:\dev\python\seo-tool\conf\GCG_Analytics_2017 YTD_20170.xlsx", "sourcedetail", "Feb")
# page_visits_tool.import_month_page_visits("Analytics", "seo_page_visits", "D:\dev\python\seo-tool\conf\GCG_Analytics_2017 YTD_20170.xlsx", "sourcedetail", "Mar")
# page_visits_tool.import_month_page_visits("Analytics", "seo_page_visits", "D:\dev\python\seo-tool\conf\GCG_Analytics_2017 YTD_20170.xlsx", "sourcedetail", "Apr")
# page_visits_tool.import_month_page_visits("Analytics", "seo_page_visits", "D:\dev\python\seo-tool\conf\GCG_Analytics_2017 YTD_20170.xlsx", "sourcedetail", "May")

# urls = ["/analytics/cn/zh",
#         "/analytics/cn/zh/technology/spss",
#         "/analytics/cn/zh/technology/spss/spss-trials.html",
#         "/software/products/zh/spss-modeler",
#         "/software/products/zh/spss-statistics",
#         "/analytics/cn/zh/technology/products/cognos-analytics.html",
#         "/analytics/watson-analytics/cn-zh/index.html",
#         "/analytics/cn/zh/technology/db2",
#         "/analytics/cn/zh/technology/db2/db2-linux-unix-windows.html",
#         "/analytics/cn/zh/technology/db2/purescale",
#         "/analytics/cn/zh/technology/hadoop",
#         "/analytics/cn/zh/technology/agile",
#         "/analytics/cn/zh/technology/data-integration",
#         "/analytics/cn/zh/technology/master-data-management",
#         "/software/products/zh/ibminfodata",
#         "ibm.com%"]
#
# page_visits_tool.page_visits_report("Analytics", "seo_page_visits", urls,
#                                     "D:\dev\python\seo-tool\out\\report\Analytics_visits_report.csv")


# page_visits_tool.import_month_page_visits("GTS", "seo_gts_page_visits", "D:\dev\python\seo-tool\conf\GCG_GTS_2017 YTD_20170531.xlsx", "sourcedetail", "Jan")
# page_visits_tool.import_month_page_visits("GTS", "seo_gts_page_visits", "D:\dev\python\seo-tool\conf\GCG_GTS_2017 YTD_20170531.xlsx", "sourcedetail", "Feb")
# page_visits_tool.import_month_page_visits("GTS", "seo_gts_page_visits", "D:\dev\python\seo-tool\conf\GCG_GTS_2017 YTD_20170531.xlsx", "sourcedetail", "Mar")
# page_visits_tool.import_month_page_visits("GTS", "seo_gts_page_visits", "D:\dev\python\seo-tool\conf\GCG_GTS_2017 YTD_20170531.xlsx", "sourcedetail", "Apr")
# page_visits_tool.import_month_page_visits("GTS", "seo_gts_page_visits", "D:\dev\python\seo-tool\conf\GCG_GTS_2017 YTD_20170531.xlsx", "sourcedetail", "May")

urls = ["/services/cn/zh/it-services/gts-it-service-home-page-1.html%",
        "/services/cn/zh/it-services/enterprise-mobility/index.html%",
        "/services/cn/zh/it-services/networking-services/index.html%",
        "/services/cn/zh/it-services/networking-services/software-defined-network",
        "/services/cn/zh/it-services/business-continuity/index.html%",
        "/services/cn/zh/it-services/business-continuity/resiliency-as-a-service/index.html%",
        "/services/cn/zh/it-services/business-continuity/ibm-cloud-resiliency-orchestration",
        "/services/cn/zh/it-services/systems/index.html%",
        "/services/cn/zh/it-services/systems/managed-services/index.html%",
        "/services/cn/zh/it-services/server-services",
        "/services/cn/zh/it-services/server-services/integrated-managed-infrastructure-services/index.html%",
        "/services/cn/zh/it-services/technical-support-services",
        "/services/cn/zh/it-services/technical-support-services/multivendor-it-support/index.html",
        "/services/cn/zh/it-services/technical-support-services/ibm-hardware-and-software-support/index.html",
        "ibm.com%"]

page_visits_tool.page_visits_report("GTS", "seo_gts_page_visits", urls,
                                    "D:\dev\python\seo-tool\out\\report\GTS_visits_report.csv")