import ujson
import codecs
from datetime import datetime
from time import time
import copy


def log_msg(message):
    """現在時刻と一緒にログを表示"""
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message)


def load_json(filename):
    with codecs.open(filename, mode='r', encoding='utf8', errors='ignore') as f:
        data = ujson.load(f)
        return data


def counter(www_path):
    dataset = load_json(www_path)
    features = ['key', 'author', 'title', 'url', 'note']
    all_result = {'key': 0, 'author': 0, 'title': 0, 'url': 0, 'note': 0}
    part_result = copy.deepcopy(all_result)
    author_counter = {}

    for record in dataset:
        for feature in features:
            all_result[feature] += 1
            if record[feature]:
                part_result[feature] += 1
            if feature == 'author':
                author_counter.setdefault(len(record[feature]), 0)
                author_counter[len(record[feature])] += 1

    result = {}
    for feature in features:
        result[feature] = f"{part_result[feature]} in {all_result[feature]}, " \
                          f"{round(part_result[feature]/all_result[feature]*100, 2)}"

    print(result)
    print(1 - author_counter[1]/all_result['author'])



def main():
    www_path = 'dataset/www.json'
    counter(www_path)




if __name__=='__main__':
    main()