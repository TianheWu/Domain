import joblib

from __Domain_process import write_data, split_domain, extract_illegal_word, construct_illegal_word_type


write_data()
char_dic = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
for i in char_dic:
    split_domain(i)


extract_illegal_word()

vocab_illegal = []
f = open(r'./illegal_word_set/illegal_word.txt', encoding='UTF-8')
for line in f.readlines():
    vocab_illegal.append(line.strip('\n'))
print(vocab_illegal)
joblib.dump(vocab_illegal, './illegal_word_set/vocab_illegal.pkl')

construct_illegal_word_type()
