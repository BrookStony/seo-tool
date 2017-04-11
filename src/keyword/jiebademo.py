#encoding=utf-8
import jieba

# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print("Full Mode:", "/ ".join(seg_list))  # 全模式
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print("Default Mode:", "/ ".join(seg_list))  # 精确模式
#
# seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
# print(type(seg_list))
# # print(len(seg_list))
# print(", ".join(seg_list))
#
# seg_list = jieba.cut_for_search("IBM认知计算帮助认知商务车辆网小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
# print(", ".join(seg_list))


jieba.load_userdict("D:\dev\python\seo-tool\conf\dict.txt")
seg_list = jieba.cut_for_search("IBM认知云计算解决方案")  # 搜索引擎模式
print(", ".join(seg_list))