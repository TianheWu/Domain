import time

from __Args import *
from __Domain_process import generate_random_domain, is_domain


num_generator_domain_valid = 0
num_generator_domain = 0
valid_domain = []
start_time = time.time()
while num_generator_domain_valid < GENERATED_DOMAIN_NUM:
    # modify here
    generator_domain = generate_random_domain(4)
    print('random domain', generator_domain)
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