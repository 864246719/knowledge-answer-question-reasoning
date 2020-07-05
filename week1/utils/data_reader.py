from collections import defaultdict
import os
from collections import Counter
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAD_TOKEN = 'PAD'
GO_TOKEN = 'GO'
EOS_TOKEN = 'EOS'
UNK_TOKEN = 'UNK'

def save_word_dict(vocab, save_path):
    with open(save_path, 'w', encoding='utf-8') as f:
        for w,i in vocab.items():
            f.write("%s\t%d\n" % (w, i))


def read_data(path_1, path_2, path_3):
    with open(path_1, 'r', encoding='utf-8') as f1, \
            open(path_2, 'r', encoding='utf-8') as f2, \
            open(path_3, 'r', encoding='utf-8') as f3:
        words = []
        # print(f1)
        for line in f1:
            words = line.split()

        for line in f2:
            words += line.split(' ')

        for line in f3:
            words += line.split(' ')

    return words

def read_vocab(input_texts, max_size=50000, min_count=5):
    token_counts = Counter()
    special_tokens = [PAD_TOKEN, GO_TOKEN, EOS_TOKEN, UNK_TOKEN]
    for line in input_texts:
        for char in line.strip():
            char = char.strip()
            if not char:
                continue
            token_counts.update(char)
    # Sort word count by value
    count_pairs = token_counts.most_common()
    vocab = [k for k, v in count_pairs if v >= min_count]
    # Insert the special tokens to the beginning
    vocab[0:0] = special_tokens
    full_token_id = list(zip(vocab, range(len(vocab))))[:max_size]
    vocab2id = dict(full_token_id)
    return vocab2id


def build_vocab(items, sort=True, min_count=0, lower=False):
    """
    构建词典列表
    :param items: list  [item1, item2, ... ]
    :param sort: 是否按频率排序，否则按items排序
    :param min_count: 词典最小频次
    :param lower: 是否小写
    :return: list: word set
    """
    result = []
    if sort:
        # sort by count
        # dic = defaultdict(int)
        dic = Counter()                                     
        for item in items:
            for i in item.split(" "):
                i = i.strip()
                if not i: continue
                i = i if not lower else item.lower()
                dic.update(i)
        # sort
        """
        按照字典里的词频进行排序，出现次数多的排在前面
        your code(one line)
        """
        count_pairs = dic.most_common()
        vocab1 = [k for k, v in count_pairs if v >= min_count]
        special_tokens = [PAD_TOKEN, GO_TOKEN, EOS_TOKEN, UNK_TOKEN]
        vocab1[0:0] = special_tokens
        full_token_id = list(zip(vocab1, range(len(vocab1))))[min_count:5000]
        vocab = dict(full_token_id)

        # for i, item in enumerate(dic1):
        #     key = item[0]
        #     if min_count and min_count > item[1]:
        #         continue
        #     result.append(key)
        
    else:
        # sort by items
        for i, item in enumerate(items):
            item = item if not lower else item.lower()
            result.append(item)
    """
    建立项目的vocab和reverse_vocab，vocab的结构是（词，index）
    your code
    vocab = (one line)
    reverse_vocab = (one line)
    """
    reverse_vocab = {}

    for k,v in  vocab.items():
        reverse_vocab[v]=k

    return vocab ,reverse_vocab


if __name__ == '__main__':
    lines = read_data('{}/datasets/train_set.seg_x.txt'.format(BASE_DIR),
                      '{}/datasets/train_set.seg_y.txt'.format(BASE_DIR),
                      '{}/datasets/test_set.seg_x.txt'.format(BASE_DIR))
    vocab, reverse_vocab = build_vocab(lines)
    save_word_dict(vocab, '{}/datasets/vocab.txt'.format(BASE_DIR))