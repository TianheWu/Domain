import numpy as np

from numpy.lib.npyio import save


class Preprocessing:

    @staticmethod
    def read_dataset():
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                    '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        f = open(r'danger_domain/danger_domain_z.txt', encoding='UTF-8')
        raw_text = f.readlines()
        raw_text = [line.lower().strip('\n')[:-4] for line in raw_text]
        text_string = ''
        sum = 0
        idx = 0
        for line in raw_text:
            text_string += line.strip()
            sum += len(line)
            idx += 1
        text = list()
        for char in text_string:
            text.append(char)
        text = [char for char in text if char in letters]
        # print("average = ", int(sum / idx))
        return text

    @staticmethod
    def create_dictionary(text):
        char_to_idx = dict()
        idx_to_char = dict()
        idx = 0
        for char in text:
            if char not in char_to_idx.keys():
                char_to_idx[char] = idx
                idx_to_char[idx] = char
                idx += 1
        return char_to_idx, idx_to_char

    @staticmethod
    def build_sequences_target(text, char_to_idx, window):
        x = list()
        y = list()
        for i in range(len(text)):
            try:
                sequence = text[i:i + window]
                sequence = [char_to_idx[char] for char in sequence]
                target = text[i + window]
                target = char_to_idx[target]
                x.append(sequence)
                y.append(target)
            except:
                pass
        x = np.array(x)
        y = np.array(y)
        return x, y



