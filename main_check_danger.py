import joblib

from __Domain_process import get_context_from_url, cut_text_word
from __Args import *


domain_text = {}
count_url = 0
index = 0
f = open(r'./generated_domain/generated_domains_c.txt', encoding='UTF-8')
for line in f.readlines():
    index += 1
    if line not in domain_text:
        line = line.strip('\n')
        context = get_context_from_url(line, index)
        domain_text[line] = context
        if len(context) != 0:
            count_url += 1

print('Success rate of crawling web pages', count_url / index, '\n')
joblib.dump(domain_text, './domain_text/domain_text_dict' + '_c.pkl')

danger_domain = []
domain_word_freq = {}
illegal_domain_word = {}
threshold = 0.06

vocab_illegal = joblib.load('./illegal_word_set/vocab_illegal.pkl')
for key, val in domain_text.items():
    word_freq = 0
    sentence_include_flag = False
    for sentence in val:
        sentence.replace('！', '').replace('，', '').replace('。', '').replace('；', '')
        word_list = cut_text_word(sentence).split('/')
        for word in word_list:
            if word in vocab_illegal:
                word_freq += 1
                print('illegal word', word)
                if key not in illegal_domain_word:
                    illegal_domain_word[key] = [word]
                else:
                    illegal_domain_word[key].append(word)
                if key not in danger_domain:
                    danger_domain.append(key)
                sentence_include_flag = True
                break
    if sentence_include_flag:
        domain_word_freq[key] = word_freq / len(val)
        if domain_word_freq[key] < threshold:
            illegal_domain_word.pop(key)

joblib.dump(illegal_domain_word, './illegal_word_set/generated_domain_word/illegal_domain_word' + '_c.pkl')

print("Danger domains:", danger_domain)
print('Word frequence', domain_word_freq)
print('Illegal domain word', illegal_domain_word)
print('Illegal domain percentage', len(danger_domain) / 10)