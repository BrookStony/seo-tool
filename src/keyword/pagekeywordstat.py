import jieba

class PageKeywordStat():

    def stat_keywords(self, url, page, keywords):
        print("<stat_keywords> ur: " + url + ", keywords=" + str(keywords))
        keyword_stat_map = {}
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
                print(keyword)
                keyword_times = 0
                for line in lines:
                    # print("line=" + line)
                    if keyword in line:
                        keyword_times += 1
                print(keyword_times)
                if keyword_times > 0:
                    keyword_stat_map.setdefault(keyword, keyword_times)
                else:
                    keyword_times = self.phrase_match(lines, keyword)
                    if keyword_times > 0:
                        print("phraseMatch=" + keyword)
                        keyword_stat_map.setdefault(keyword, keyword_times)
                    else:
                        not_match_keywords.append(keyword)
            print(keyword_stat_map)
            print(not_match_keywords)
        except Exception as e:
            print(e)
        return keyword_stat_map, not_match_keywords

    # 短语匹配
    def phrase_match(self, lines, keyword):
        match_times = 0
        words = jieba.cut_for_search(keyword)
        start = 0
        words_count = 0
        word_list = []
        for word in words:
            words_count += 1
            word_list.append(word)

        print(word_list)

        for line in lines:
            print("line: " + line)
            for i in range(start, words_count):
                word = word_list[i]
                if word in line:
                    print("word: " + word)
                    start = i + 1
                else:
                    break
            if start == words_count:
                start = 0
                match_times += 1

        return match_times