import jieba

class KeywordEngine():

    def stat_page_keywords(self, url, page, keywords):
        """统计页面关键词
        """
        print("<stat_page_keywords> url: " + url + ", keywords=" + str(keywords))
        match_keywords = []
        not_match_keywords = []
        try:

            lines = []
            split_lines = page.splitlines()
            for line in split_lines:
                line = line.strip()
                if '' != line:
                    lines.append(line)

            exact_match_map = {}
            phrase_match_map = {}
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
            phrase_match_keywords = self.sort_keywords(phrase_match_map)
            match_keywords.extend(phrase_match_keywords)
        except Exception as e:
            print(e)
        return match_keywords, not_match_keywords

    def sort_keywords(self, keywords_map):
        keywords = []
        keywords_list = []
        for (k, v) in keywords_map.items():
            keywords_list.append((k, v))
        # 排序
        keywords_list.sort(key=lambda x: x[1], reverse=True)
        for words in keywords_list:
            keywords.append(words[0])
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