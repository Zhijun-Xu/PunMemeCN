# -*- coding:utf-8 -*-
from pypinyin import pinyin, lazy_pinyin
from Pinyin2Hanzi import DefaultDagParams, dag


def chinese_character_to_pinyin(chinese_text:str, pattern:str='normal'):
    """
    Convert Chinese characters into pinyin
    pattern = 'normal' or 'lazy'
    """
    assert pattern in ['lazy', 'normal']
    if pattern == 'lazy':
        chinese_pinyin = [i for i in lazy_pinyin(chinese_text)]
    else:
        chinese_pinyin = [i[0] for i in pinyin(chinese_text)]
    return chinese_pinyin


def retrieve_homophonic_sentence(chinese_text:str):
    """
    Retrieve the most likely homophonic sentence for the current chinese sentence
    """
    # Keep the purely Chinese parts of the sentence
    hanzi_index = []
    hanzi_text = []
    for i in range(len(chinese_text)):
        if '\u4e00' <= chinese_text[i] <= '\u9fff':
            hanzi_index.append(i)
            hanzi_text.append(chinese_text[i])
    # Convert Chinese parts into lazy pinyin
    pinyin_text = chinese_character_to_pinyin(''.join(hanzi_text), pattern='lazy')
    # Convert lazy pinyin to most likely Chinese characters
    dagparams = DefaultDagParams()
    hanzi_text = dag(dagparams, pinyin_text, path_num=2)[0].path
    hanzi_text = list(''.join(hanzi_text))
    # Get the homophonic sentence
    chinese_text = list(chinese_text)
    for i in range(len(hanzi_text)):
        chinese_text[hanzi_index[i]] = hanzi_text[i]
    chinese_text = ''.join(chinese_text)
    return chinese_text
