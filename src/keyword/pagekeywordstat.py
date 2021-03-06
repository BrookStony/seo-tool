import jieba
from operator import itemgetter, attrgetter

class PageKeywordStat():

    def stat_keywords(self, url, page, keywords):
        print("<stat_keywords> ur: " + url + ", keywords=" + str(keywords))
        exact_match_map = {}
        phrase_match_map = {}
        match_keywords = []
        not_match_keywords = []
        try:
            # print(page_text)
            lines = []
            split_lines = page.splitlines()
            for line in split_lines:
                line = line.strip()
                if '' != line:
                    lines.append(line)

            for keyword in keywords:
                keyword_times = 0
                for line in lines:
                    # print("line=" + line)
                    if keyword in line:
                        keyword_times += 1
                if keyword_times > 0:
                    exact_match_map.setdefault(keyword, keyword_times)
                else:
                    keyword_times = self.phrase_match(lines, keyword)
                    if keyword_times > 1:
                        print("phraseMatch=" + keyword)
                        phrase_match_map.setdefault(keyword, keyword_times)
                    else:
                        not_match_keywords.append(keyword)

            print(exact_match_map)
            print(phrase_match_map)
            print(not_match_keywords)
            match_keywords = self.sort_keywords(exact_match_map)
            phrase_match_list = self.sort_keywords(phrase_match_map)
            match_keywords.extend(phrase_match_list)
        except Exception as e:
            print(e)
        return match_keywords, not_match_keywords

    def sort_keywords(self, match_map):
        keywords = []
        keywords_list = []
        for (k, v) in match_map.items():
            keywords_list.append((k, v))
        print("=======1==========")
        print(keywords_list)
        # sorted(keywords_list, key=itemgetter(1), reverse=True)
        keywords_list.sort(key=lambda x: x[1], reverse=True)
        print("=========2========")
        # keywords_list.sort()
        print(keywords_list)
        for words in keywords_list:
            keywords.append(words[0])
        print(keywords)
        return keywords

    # 短语匹配
    def phrase_match(self, lines, keyword):
        match_times = 0
        words = jieba.cut_for_search(keyword)
        start = 0
        words_count = 0
        word_list = []
        for word in words:
            if len(word) > 1:
                words_count += 1
                word_list.append(word)

        for line in lines:
            for i in range(start, words_count):
                word = word_list[i]
                if word in line:
                    # print("line: " + line)
                    # print("word: " + word)
                    start = i + 1
                else:
                    break
            if start == words_count:
                start = 0
                match_times += 1

        return match_times