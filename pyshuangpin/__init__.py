from pyshuangpin.scheme import Scheme, xiaohe, ziranma, sogou, microsoft, znabc

import pypinyin


def shuangpin(hans, scheme: Scheme, **kwargs):
    pinyin = pypinyin.pinyin(hans, **kwargs)
    if scheme == Scheme.Xiaohe:
        scheme_dict = xiaohe.scheme
    elif scheme == Scheme.Ziranma:
        scheme_dict = ziranma.scheme
    elif scheme == Scheme.Sogou:
        scheme_dict = sogou.scheme
    elif scheme == Scheme.Microsoft:
        scheme_dict = microsoft.scheme
    elif scheme == Scheme.ZNABC:
        scheme_dict = znabc.scheme
    else:
        raise NotImplementedError('scheme not implemented')

    for key, value in scheme_dict.items():
        for item in pinyin:
            for index in range(len(item)):
                item[index] = item[index].replace(key, value)

    return pinyin
