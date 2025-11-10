# -*- coding:utf-8 -*-
import os
import json
from copy import deepcopy

def load_json_file(file_path):
    if os.path.exists(file_path):
        f = open(file_path, 'r', encoding='utf-8')
        file = json.load(f); f.close()
    else:
        file = dict()
    return file


def save_json_file(file, file_path):
    f = open(file_path, 'w', encoding='utf-8')
    json.dump(file, f, indent=4, ensure_ascii=False)
    f.close()


def load_jsonl_file(file_path):
    file = []
    if os.path.exists(file_path):
        f = open(file_path, 'r', encoding='utf-8')
        for line in f:
            file.append(json.loads(line))
        f.close()
    return file


def save_jsonl_file(file, file_path):
    f = open(file_path, 'w', encoding='utf-8')
    for data in file:
        line = json.dumps(data, ensure_ascii=False)
        f.write(line + '\n')
    f.close()


def extend_dict(dictionary, key_list):
    dictionary = deepcopy(dictionary)
    temp = dictionary
    for i in range(len(key_list)):
        sub_key = key_list[i]
        if sub_key not in temp:
            temp[sub_key] = dict()
        temp = temp[sub_key]
    return dictionary
