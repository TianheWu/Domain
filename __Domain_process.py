import random
import string
from func_timeout.StoppableThread import JoinThread
import joblib
import numpy
import requests
import jieba

from openpyxl import load_workbook
from urllib import request
from func_timeout import func_set_timeout
from lxml import etree
from bs4 import BeautifulSoup
from selenium import webdriver


def write_data():
    data = load_workbook('table.xlsx')
    sheet = data.get_sheet_by_name('Sheet1')
    domain = sheet['A']
    label = sheet['B']
    domain_text = []
    label_text = []
    for x in range(1, len(domain)):
        domain_text.append(domain[x].value)
    for x in range(1, len(label)):
        label_text.append(label[x].value)
    danger_text = []
    save_text = []
    unknow_text = []
    for i in range(len(domain_text)):
        if label_text[i] == '未知':
            unknow_text.append(domain_text[i])
        elif label_text[i] == '危险':
            danger_text.append(domain_text[i])
        elif label_text[i] == '安全':
            save_text.append(domain_text[i])
    with open('save_text.txt', 'w') as f:
        for x in save_text:
            f.write(x)
    with open('unknow_text.txt', 'w') as f:
        for x in unknow_text:
            f.write(x)
    with open('danger_text.txt', 'w') as f:
        for x in danger_text:
            f.write(x)


def split_domain(domain_first_char):
    f = open(r'danger_text.txt', encoding='UTF-8')
    danger_domain_d = []
    for line in f.readlines():
        if line[0] == domain_first_char:
            danger_domain_d.append(line)
    new_text_name = 'danger_domain_' + domain_first_char + '.txt'
    with open(new_text_name, 'w') as f_d:
        for x in danger_domain_d:
            f_d.write(x)


# pick the string included first letter
def special_select(sequences, char_to_idx, first_char):
    first_char_idx = char_to_idx[first_char]
    seq_included = []
    for i in sequences:
        if i[0] == first_char_idx:
            seq_included.append(i)
    start = numpy.random.randint(0, len(seq_included) - 1)
    select_pattern = seq_included[start]
    return select_pattern


def extract_illegal_word():
    f = open(r'./illegal_word_set/keywords.txt', encoding='UTF-8')
    illegal_word_list = []
    for line in f.readlines():
        line = line.strip().split()
        illegal_word_list.append(line[0])
    with open('illegal_word.txt', 'w') as f_d:
        for i in illegal_word_list:
            f_d.write(i)
            f_d.write('\n')


def construct_illegal_word_type():
    illegal_word_type = {}
    f = open(r'./illegal_word_set/keywords.txt', encoding='UTF-8')
    for line in f.readlines():
        line = line.strip().split()
        if line[0] not in illegal_word_type:
            illegal_word_type[line[0]] = line[3]
    joblib.dump(illegal_word_type, './illegal_word_set/illegal_word_type.pkl')


@func_set_timeout(5)
def is_domain(url):
    url_1 = 'https://' + url + '/'
    url_2 = 'http://' + url + '/'
    try:
        request.urlopen(url_1)
        return True
    except Exception as e:
        try:
            request.urlopen(url_2)
            return True
        except Exception as e:
            return False


def get_url(url):
    url_1 = 'https://' + url + '/'
    url_2 = 'http://' + url + '/'
    try:
        request.urlopen(url_1)
        return url_1
    except Exception as e:
        try:
            request.urlopen(url_2)
            return url_2
        except Exception as e:
            pass


# method_1
def get_html_text(url):
    url = get_url(url)
    print('url ', url)
    str_html = requests.get(url)
    html_str = str_html.text
    # print(html_str)
    soup = BeautifulSoup(html_str, 'lxml')
    # print(soup)
    text = soup.get_text()
    my_list = text.split('\n')
    my_list = [x.strip() for x in my_list if x.strip() != '']
    for ele in my_list:
        if '\ufeff' in my_list:
            my_list.remove('\ufeff')
    return my_list


# method_2
def get_context_from_url(url, index):
    context_list = []
    url = get_url(url)
    print('Crawl web', index, url, 'page information')
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--window-size=1920,1050")
    chrome_options.add_argument('headless')
    try:
        driver = webdriver.Chrome("/home/nslab/Domain/chromedriver", chrome_options=chrome_options)
        driver.get(url)
        pageSource = driver.page_source
        driver.close()
        soup = BeautifulSoup(pageSource, 'lxml')
        text = soup.get_text()
        context_list = text.split('\n')
        context_list = [x.strip() for x in context_list if x.strip() != '']
    except:
        pass
    return context_list


def generate_random_domain(len) -> str: 
    str1 = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(len))
    str1 = ''.join([str1, '.com'])
    return str1


def cut_text_word(sentences):
    seg_list = jieba.cut(sentences, cut_all=True)
    return '/'.join(seg_list)
