import torch
import time
import joblib

from __Model import TextGenerator
from __Args import *
from __Execution import Execution
from __Domain_process import is_domain


args = Args_lstm()
execution = Execution(args)
execution.prepare_data()
vocab_size = execution.vocab_size
model = TextGenerator(args, vocab_size)
model.load_state_dict(torch.load('./danger_domain_model_lstm/model_danger_z.pkl'))
num_generator_domain_valid = 0
num_generator_domain = 0
valid_domain = []
start_time = time.time()
while num_generator_domain_valid < GENERATED_DOMAIN_NUM:
    # modify here
    generator_domain = execution.generator(model, GENERATED_STR_NUM, 'z')
    num_generator_domain += 1
    try:
        if is_domain(generator_domain):
            if generator_domain not in valid_domain:
                valid_domain.append(generator_domain)
                num_generator_domain_valid += 1
            print('Valid domain!')
        else:
            print('Invalid domain...')
    except:
        print('Invalid domain...')
    print(num_generator_domain_valid, 'valid domain |', num_generator_domain, 'domain | percentage:', num_generator_domain_valid / num_generator_domain, "\n")
end_time = time.time()

print("Generate", GENERATED_DOMAIN_NUM, "domains", end_time - start_time, 'seconds')
print("Generated domains are:", valid_domain)

with open('./generated_domain/generated_domains_z.txt', 'w') as f:
    for x in valid_domain:
        f.write(x + '\n')

