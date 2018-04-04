import argparse
import re
import glob
import sys
import pickle

Dictionary = {}
a = []


# разбиваем строку на слова, опционально приводим к нижнему регистру
def correct_line(line, lowercase):
    line = re.sub(r'[^A-Za-zА-Яа-я ]', '', line)
    line = re.sub(r'\s+', ' ', line)
    if lowercase:
        line = line.lower
    line.strip()
    a = line.split()
    return a


# создаем словарь {слово1 : {слово2 : частота...}...}
def create_dict(a, dictionary):
    flag = 0
    global ending_word
    for i in range(len(a)):
        word2 = a[i]
        if flag == 0:
            word1 = ending_word
        elif flag == len(a) - 1:
            word1 = a[i - 1]
            ending_word = word2
        else:
            word1 = a[i - 1]
        if word1 != "":
            if dictionary.get(word1) is not None:
                if dictionary.get(word1).get(word2) is not None:
                    dictionary.get(word1)[word2] += 1
                else:
                    dictionary.get(word1).setdefault(word2, 1)
            else:
                default = {word2: 1}
                dictionary.setdefault(word1, default)
        flag += 1
    return dictionary


parser = argparse.ArgumentParser(description='Create a model.')
parser.add_argument(
    '--input-dir',
    dest='inp',
    default='stdin',
    help='input a path to the directory (else stdin)')
parser.add_argument(
    '--model',
    dest='mo',
    required=True,
    help='input a path to the file with model')
parser.add_argument(
    '--lc',
    action='store_true',
    default=False,
    help='converts text to lowercase')
args = parser.parse_args()
lowercase = args.lc

if args.inp != 'stdin':
    path = args.inp
    # извлекаем все файлы из указанной директории
    files = glob.glob(pathname=path)
    for name in files:
        ending_word = ''
        with open(name, encoding='ANSI') as f:
            for line in f:
                a = correct_line(line, lowercase)
                Dictionary = create_dict(a, Dictionary)
else:
    ending_word = ''
    for line in sys.stdin:
        correct_line(line, lowercase)
        Dictionary = create_dict(a, Dictionary)
model = args.mo
with open(model, 'wb') as t:    # сохраняем словарь в указанный файл
    pickle.dump(Dictionary, t)
