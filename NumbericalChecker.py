import num2words
import cn2an
class NumbericalChecker():
    def __init__(self,language):
        """
        :param language: e.g. 'en'
        """
        self.language = language
        self.tokenizer = self.get_tokenizer(language)
        self.decial_thousands_language_list = 'de'
        self.number_word_list = []
        if language == 'en':
            numbers = []
            for i in range(0, 100):
                numbers.append(self.num2words(i))
            self.number_word_list = numbers + ['hundred', 'thousand', 'million', 'billion', 'trillion']
        if language == 'zh':
            for i in range(0,10):
                self.number_word_list.append(str(i))
                self.number_word_list.append(cn2an.an2cn(i))

            self.number_word_list+=['百','千','万','亿','兆']
    def get_tokenizer(self,lang):
        if lang == 'zh':
            pass
        if lang == 'en':
            from nltk.tokenize import word_tokenize
            return word_tokenize
            pass
        if lang == 'de':
            pass
        if lang == 'ne':
            pass
        if lang == 'ta':
            pass
    def check(self,sentence,number):
        """
        :param sentence: str; sentence need to be check
        :param number: int; the number that the sentence needs to be include
        :return: boolean; does the sentence contain the correct number
        """
        words = self.num2words(number)
        correct_translation=[str(number),self.add_thousands_separators(number),words]  + self.words_list(words)
        correctness = False
        for t in correct_translation:
            if t.lower() in sentence.lower():
                if self.check_extra(t.lower(),sentence.lower()):
                    correctness = True
            else:
                if self.language == 'zh' or self.language == 'de':
                    if t.lower() in sentence.lower().replace(" ","").replace(",",""):
                        if self.check_extra(t.lower(), sentence.lower().replace(" ","").replace(",","")):
                            correctness = True
        return correctness

    def num2words(self, number):
        if self.language == 'en' or self.language == 'de':
            return num2words.num2words(number,lang = self.language)
        if self.language =='zh':
            return cn2an.an2cn(number)


    def add_thousands_separators(self,number):
        """
        :param number: float; "123" or "123.5"
        :param language: str; 'en'/'de'
        :return:the number that seperated by thousands separators
        """
        number_string = "{:,}".format(number)

        if self.language in self.decial_thousands_language_list:
            number_string = number_string.replace(",","_").replace(".",",").replace("_",".")
        return number_string

    def words_list(self,words):
        """

        :param words: str; words form of number
        :return: list; all acceptable words form
        """
        if self.language == 'en':
            return self.words_list_en(words)
        if self.language == 'zh':
            return self.words_list_zh(words)
        if self.language == 'de':
            return self.words_list_de(words)

    def words_list_zh(self,words):
        word_list = [""]
        zh_uni = ["亿", "万", "千", "百"]
        for i in words:
            if i == "二" or i == "两":
                length = len(word_list)
                for idx in range(0, length):
                    string = word_list[idx]
                    word_list[idx] = string + "二"
                    word_list.append(string + "两")
            else:
                if i in zh_uni:
                    length = len(word_list)
                    for idx in range(0, length):
                        string = word_list[idx]
                        word_list[idx] = string + i
                        word_list.append(string + i + ",")
                        word_list.append(string + i + "、")
                        word_list.append(string + i + "，")
                else:
                    length = len(word_list)
                    for idx in range(0, length):
                        word_list[idx] = word_list[idx] + i
        length = len(word_list)
        for num in range(0, length):
            word = word_list[num]
            if word.endswith("点零"):
                word_list.append(word.replace("点零", ""))
        return word_list

    def words_list_de(selfs,words):
        word_list = [words]
        length = len(word_list)

        for i in range(0,length):
            w = word_list[i]
            word_list.append(w.replace("hundert", "hundert "))
            word_list.append(w.replace("hundert", "hundertund"))
            word_list.append(w.replace("hundert", "hundert und "))
        for i in range(0,length):
            w = word_list[i]
            word_list.append(w.replace("tausend", "tausend und "))
            word_list.append(w.replace("tausend", "tausendund "))
            word_list.append(w.replace("tausend", "tausend "))
        for i in range(0,length):
            w = word_list[i]
            word_list.append(w.replace("Komma", "Punkt"))
        for i in range(0,length):
            w = word_list[i]
            word_list.append(w.replace("einhundert", "hundert"))
            word_list.append(w.replace("eintausend", "tausend"))
        return word_list

    def words_list_en(self, words):
        token_list =  self.tokenizer(words)
        words_list = [""]
        for idx, t in enumerate(token_list):
            if t == "and" or t == ',':
                length = len(words_list)
                for ind in range(0, length):
                    w = words_list[ind]
                    words_list[ind] = w + " and"
                    words_list.append(w + ",")
                    words_list.append(w)
            else:
                if t == 'point':
                    length = len(words_list)
                    for ind in range(0, length):
                        w = words_list[ind]
                        words_list[ind] = w + " point"
                        words_list.append(w + " dot")
                        words_list.append(w)
                else:
                    if t == '-':
                        length = len(words_list)
                        for ind in range(0, length):
                            w = words_list[ind]
                            words_list[ind] = w + "-"
                            words_list.append(w + " -")
                            words_list.append(w)
                    else:
                        if '-' in t:
                            length = len(words_list)
                            for ind in range(0, length):
                                w = words_list[ind]
                                words_list[ind] = w + " " + t
                                words_list.append(w + " " + t.replace("-"," "))
                        else:
                            for ind, w in enumerate(words_list):
                                words_list[ind] = w + " " + t
        return [w.strip() for w in words_list]

    def check_extra(self,t,sentence):
        if self.language == 'en':
            return self.check_extra_en(t,sentence)
        if self.language == 'zh':
            return self.check_extra_zh(t,sentence)
        if self.language == 'de':
            return True

    def check_extra_zh(self,t,sentence):
        head_index = sentence.index(t)
        tail_index = head_index + len(t) -1
        if head_index -1 >=0:
            if sentence[head_index-1] in self.number_word_list:
                return False
        if tail_index +1 <len(sentence):
            if not sentence[tail_index +1] in self.number_word_list:
                if sentence[tail_index+1] == '.':
                    if tail_index+2 <len(sentence):
                        return not sentence[tail_index+2] in self.number_word_list
                return True
        return True

    def check_extra_en(self,t, sentence):
        replace_sentence = sentence.replace(t, "|||||")
        tokens = self.tokenizer(replace_sentence)
        try:
            ind = tokens.index("|||||")
        except:
            return False

        search_done = False
        correctness = False
        while not search_done:
            ind = ind - 1

            if ind < 0:
                correctness = True
                search_done = True
            else:
                token = tokens[ind]
                if token in self.number_word_list:
                    return False
                if token != "and" and token != ",":
                    correctness = True
                    search_done = True
        search_done = False
        ind = tokens.index("|||||")
        while not search_done:
            ind = ind + 1
            if ind > len(tokens)-1:
                correctness = True
                search_done = True
            else:
                token = tokens[ind]
                if token in self.number_word_list:
                    return False
                if token != "and" and token != ",":
                    correctness = True
                    search_done = True
        return correctness
# checker = NumbericalChecker('de')
# print(checker.check("Gesamt ist 100.245 ",100245))
