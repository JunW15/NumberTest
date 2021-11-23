""" Usage:
    NumbericalEvaluation.py --src --tgt --model --template_folder_path
"""
import json
from docopt import docopt
import random
import num2words
import cn2an
import os
from google_translate import google_translate
from NumbericalChecker import NumbericalChecker
import sys
decial_thousands_language_list = ['de']

def add_thousands_separators(number,language):
    """
    :param number: float; "123" or "123.5"
    :param language: str; 'en'/'de'
    :return:the number that seperated by thousands separators
    """
    number_string = "{:,}".format(number)
    if language in decial_thousands_language_list:
        number_string = number_string.replace(",", "_").replace(".", ",").replace("_", ".")
    return number_string
def read_template(path):
    with open(path) as f:
        templates = json.load(f)
    return templates

def int_generator(max_digits=10, num_each_digits=5):
    number_set = []
    number_ori = []
    for digits in range(0,max_digits):
        for _ in range(0,num_each_digits):
            num = random.randint(pow(10, digits), pow(10, digits + 1))
            while num in number_set:
                num = random.randint(pow(10, digits), pow(10, digits + 1))
            number_set.append(num)
            number_ori.append(num)
    return number_set,number_ori

def sep_generator(language, max_digits=10, num_each_digits=5):
    number_set = []
    number_ori = []
    for digits in range(4,max_digits):
        for _ in range(0,num_each_digits):
            dec = random.randint(0,4)
            num = round(random.uniform(pow(10,digits-1),pow(10,digits)), dec)
            num_sep = add_thousands_separators(num,language)
            while num in number_set:
                dec = random.randint(0, 4)
                num = round(random.uniform(pow(10, digits - 1), pow(10, digits)), dec)
                num_sep = add_thousands_separators(num, language)
            number_set.append(num_sep)
            number_ori.append(num)
    return number_set,number_ori

def dec_generator(int_digits = 4, dec_digits = 5, num_each_digits = 5):
    number_set = []
    number_ori = []
    for dec_d in range(1,dec_digits):
        for int_d in range(0,int_digits):
            for _ in range(0,num_each_digits):
                if int_d == 0:
                    num = round(random.uniform(0,1), dec_d)
                else:
                    num = round(random.uniform(pow(10,int_d-1),pow(10,int_d)), dec_d)
                while num in number_set:
                    if int_d == 0:
                        num = round(random.uniform(0, 1), dec_d)
                    else:
                        num = round(random.uniform(pow(10, int_d - 1), pow(10, int_d)), dec_d)
                number_ori.append(num)
                number_set.append(num)
    return number_set,number_ori

def num2word_en(number):
    return num2words.num2words(number,lang = 'en')

def num2word_de(number):
    return num2words.num2words(number,lang = 'de')

def num2word_zh(number):
    return cn2an.an2cn(number)

def word_generator(language, int_digits = 10, num_each_digits = 5):
    number_set = []
    number_ori = []
    for digtis in range(4, int_digits):
        for _ in range(0, num_each_digits):
            d = random.randint(0, 1)
            if d == 0:
                num = random.randint(pow(10, digtis - 1), pow(10, digtis))
            else:
                dec = random.randint(0, 4)
                num = round(random.uniform(pow(10, digtis - 1), pow(10, digtis)), dec)
            if language == 'en':
                num_word = num2word_en(num)
            if language == 'de':
                num_word = num2word_de(num)
            if language == 'zh':
                num_word = num2word_zh(num)
            while num in number_set:
                d = random.randint(0, 1)
                if d == 0:
                    num = random.randint(pow(10, digtis - 1), pow(10, digtis))
                else:
                    dec = random.randint(0, 4)
                    num = round(random.uniform(pow(10, digtis - 1), pow(10, digtis)), dec)
                if language == 'en':
                    num_word = num2word_en(num)
                if language == 'de':
                    num_word = num2word_de(num)
                if language == 'zh':
                    num_word = num2word_zh(num)

            number_set.append(num_word)
            number_ori.append(num)
    return number_set,number_ori

def generate_test_case(templates,number_generator):
    test_set = {}
    number_set,number_ori = number_generator
    for idx,number in enumerate(number_set):
        t = random.randint(0,len(templates) - 1)
        test_set[number_ori[idx]] = {'tem': t, 'sent':templates[t].replace("[NUM]",str(number))}
    return test_set


def check_sets(evaluation,language):
    checker = NumbericalChecker(language)
    # results = copy.deepcopy(evauation)
    for evauation_type in evaluation:
        for num in evaluation[evauation_type]:
            translation = evaluation[evauation_type][num]['translation']
            if type(num) == str:
                if '.' in num:
                    evaluation[evauation_type][num]['evaluate_result'] = checker.check(translation, float(num))
                else:
                    evaluation[evauation_type][num]['evaluate_result'] = checker.check(translation, int(num))
            else:
                evaluation[evauation_type][num]['evaluate_result'] = checker.check(translation,num)
    return evaluation
def print_wrong_instance(evaluation):
    for evaluation_type in evaluation:
        print("================={}================".format(evaluation_type))
        for num in evaluation[evaluation_type]:
            if not evaluation[evaluation_type][num]['evaluate_result']:
                # a = evaluation[evaluation_type][num]['translation']
                # print(evaluation[evaluation_type][num]['translation'])
                print("Number is {}, translation results is {} ".format(
                    str(num),evaluation[evaluation_type][num]['translation']))

def record_results(evaluation):
    results = {}
    # print(len(evaluation))
    for evaluation_type in evaluation:
        type_results = [evaluation[evaluation_type][num]['evaluate_result'] for num in evaluation[evaluation_type]]
        results[evaluation_type] = round(sum(type_results)/len(type_results),4)
        print("{}: Pass rate is {}%.".format(evaluation_type,results[evaluation_type]*100))
    return results
def main(src,tgt,model,path):
    template_path = os.path.join(path, 'templates_' + src + '.txt')
    templates = read_template(template_path)
    number_generators = {'INT': int_generator(), 'DEC': dec_generator(), 'SEP': sep_generator(src),
                         "WORD": word_generator(src)}
    evaluation_set = {}
    sent_to_num = {}
    instances = []
    for evaluation_type in number_generators:
        evaluation_set[evaluation_type] = {}
        evaluation_set[evaluation_type] = generate_test_case(templates[evaluation_type],number_generators[evaluation_type])
        for num in evaluation_set[evaluation_type]:
            sent_to_num[evaluation_set[evaluation_type][num]['sent']] = {'type':evaluation_type,'num':num}
    for ins in sent_to_num:
        instances.append(ins)
    translation = model.translate(instances)
    for idx,ins in enumerate(instances):
        evaluation_type = sent_to_num[ins]['type']
        num = sent_to_num[ins]['num']
        evaluation_set[evaluation_type][num]['translation'] = translation[idx]
    check_sets(evaluation_set, tgt)
    record_results(evaluation_set)
    print_wrong_instance(evaluation_set)
    # return evaluation_set

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

