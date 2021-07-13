import joblib


illegal_domain_word = joblib.load('./illegal_word_set/generated_domain_word/illegal_domain_word_c.pkl')
illegal_word_type = joblib.load('./illegal_word_set/illegal_word_type.pkl')

print(illegal_domain_word)
domain_illegal_type = {}

for key, val in illegal_domain_word.items():
    val = list(set(val))
    for word in val:
        if key not in domain_illegal_type:
            domain_illegal_type[key] = []
            domain_illegal_type[key].append(illegal_word_type[word])
        if illegal_word_type[word] not in domain_illegal_type[key]:
            domain_illegal_type[key].append(illegal_word_type[word])


print(domain_illegal_type)