import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import time

from __Preprocessing import Preprocessing
from __Model import TextGenerator
from __Domain_process import special_select


class Execution:

    def __init__(self, args):
        self.window = args.window
        self.batch_size = args.batch_size
        self.learning_rate = args.learning_rate
        self.num_epochs = args.num_epochs
        self.targets = None
        self.sequences = None
        self.vocab_size = None
        self.char_to_idx = None
        self.idx_to_char = None

    def prepare_data(self):
        preprocessing = Preprocessing()
        text = preprocessing.read_dataset()
        self.char_to_idx, self.idx_to_char = preprocessing.create_dictionary(text)
        self.sequences, self.targets = preprocessing.build_sequences_target(text, self.char_to_idx, window=self.window)
        self.vocab_size = len(self.char_to_idx)

    def train(self, args):
        model = TextGenerator(args, self.vocab_size)
        optimizer = optim.RMSprop(model.parameters(), lr=self.learning_rate)
        num_batches = int(len(self.sequences) / self.batch_size)
        model.train()
        best_val_loss = float("inf")
        # use_gpu = torch.cuda.is_available()
        for epoch in range(self.num_epochs):
            start_time = time.time()
            train_num = 0
            epoch_loss = 0
            for i in range(num_batches):
                optimizer.zero_grad()
                try:
                    x_batch = self.sequences[i * self.batch_size: (i + 1) * self.batch_size]
                    y_batch = self.targets[i * self.batch_size: (i + 1) * self.batch_size]
                except:
                    x_batch = self.sequences[i * self.batch_size:]
                    y_batch = self.targets[i * self.batch_size:]
                x = torch.from_numpy(x_batch).type(torch.LongTensor)
                y = torch.from_numpy(y_batch).type(torch.LongTensor)
                y_pred = model(x)
                loss = F.cross_entropy(y_pred, y.squeeze())
                loss.backward()
                optimizer.step()
                train_num += len(x)
                epoch_loss += loss.item()
            end_time = time.time()
            epoch_loss = epoch_loss / train_num
            print("Epoch:", epoch + 1, "|", "Epoch time:", end_time - start_time, "|",  "Train_loss:", epoch_loss)
            if epoch_loss < best_val_loss:
                best_val_loss = epoch_loss
                # torch.save(model.state_dict(), 'danger_d_ep' + str(epoch + 1) + '_loss_' + str(round(best_val_loss, 5)) + '.pkl')
                torch.save(model.state_dict(), './danger_domain_model_lstm/model_danger_z.pkl')

    def generator(self, model, n_chars, first_char):
        model.eval()
        softmax = nn.Softmax(dim=1)
        # Randomly is selected the index from the set of sequences
        # start = np.random.randint(0, len(self.sequences) - 1)
        pattern = special_select(self.sequences, self.char_to_idx, first_char)
        # The pattern is defined given the random idx
        # pattern = self.sequences[start]
        print('Window selected is:', pattern)
        # By making use of the dictionaries, it is printed the pattern
        select_domain_str = ''.join([self.idx_to_char[value] for value in pattern])
        print('Selected domain string is:', select_domain_str)
        # In full_prediction we will save the complete prediction
        full_prediction = pattern.copy()
        # The prediction starts, it is going to be predicted a given
        # number of characters
        with torch.no_grad():
            for i in range(n_chars):
                # The numpy patterns is transformed into a tesor-type and reshaped
                pattern = torch.from_numpy(pattern).type(torch.LongTensor)
                pattern = pattern.view(1, -1)
                # Make a prediction given the pattern
                prediction = model(pattern)
                # It is applied the softmax function to the predicted tensor
                prediction = softmax(prediction)
                # The prediction tensor is transformed into a numpy array
                prediction = prediction.squeeze().detach().numpy()
                # It is taken the idx with the highest probability
                arg_max = np.argmax(prediction)
                # The current pattern tensor is transformed into numpy array
                pattern = pattern.squeeze().detach().numpy()
                # The window is sliced 1 character to the right
                pattern = pattern[1:]
                # The new pattern is composed by the "old" pattern + the predicted character
                pattern = np.append(pattern, arg_max)
                # The full prediction is saved
                full_prediction = np.append(full_prediction, arg_max)
        new_domain = ''.join([self.idx_to_char[value] for value in full_prediction]) + '.com'
        print("Generator domain string is:", new_domain)
        return new_domain
