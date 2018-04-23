import argparse
import random
import glob
import pickle

parser = argparse.ArgumentParser(description='Generate a text.')
parser.add_argument(
    '--model',
    dest='mo',
    required=True,
    help='input a path to the file with model')
parser.add_argument(
    '--length',
    dest='len',
    required=True,
    help='input length')
parser.add_argument(
    '--seed',
    dest='seed',
    default='0',
    help='input the first word (else random)')
parser.add_argument(
    '--output',
    dest='out',
    default='stdout',
    help='input a path to the directory (else stdout)')
args = parser.parse_args()
seed = args.seed
model = args.mo
length = int(args.len)
output = args.out


class MakeText:
    def OpenModel(self):
        model = args.mo
        with open(model, 'rb') as k:    # загружаем словарь из указанного файла
            dictionary = pickle.load(k)
        return dictionary


    def make_text(self, dictionary):
    # генерируем свой текст на основе словаря
        list_of_keys = []
        for i in dictionary.keys():
            list_of_keys.append(i)
        if seed != '0':
            begining_word = args.seed
        else:
            begining_word = random.choice(list_of_keys)
        result = []
        result.append(begining_word)
        len_of_text = args.len
        for i in range(0, int(len_of_text)):
            sum = 0
            list_of_prob = []
            for j in dictionary[result[i]].values():
                sum += int(j)
            for j in dictionary[result[i]].values():
                list_of_prob.append(int(j) / sum)
            list_of_values = []
            for j in dictionary[result[i]].keys():
                list_of_values.append(j)
            new_word = random.choices(list_of_values, weights=list_of_prob, k=1)
            result.append(new_word[0])
        return result


    def Output(self, dictionary):
        # выводим созданный  нами текст в заданный файл(иначе в stdout)
        if args.out != 'stdout':
            path = args.out
            file = glob.glob(path)
            with open(file) as f:
                text = self.make_text(dictionary)
                f.write(text)
        else:
            text = self.make_text(dictionary)
            print(' '.join(text))


x = MakeText()
_dict = x.OpenModel()
x.Output(_dict)
