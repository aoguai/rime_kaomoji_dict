# 参考 py之拼音拆分 ：https://www.jianshu.com/p/35215c6e2b8b

from Pinyin2Hanzi import DefaultHmmParams
from Pinyin2Hanzi import viterbi

hmmparams = DefaultHmmParams()


def sm(strs):
    smlist = 'bpmfdtnlgkhjqxrzcsyw'
    nosm = ['eR', 'aN', 'eN', 'iN', 'uN', 'vN', 'nG', 'NG']
    rep = {'ZH': 'Zh', 'CH': 'Ch', 'SH': 'Sh'}

    for s in smlist:
        strs = strs.replace(s, s.upper())

    for s in nosm:
        strs = strs.replace(s, s.lower())

    for s in rep.keys():
        strs = strs.replace(s, rep[s])

    for s in nosm:
        tmp_num = 0
        isOk = False
        while (tmp_num < len(strs)) and (isOk == False):
            try:
                tmp_num = strs.index(s.lower(), tmp_num)
            except:
                isOk = True
            else:
                tmp_num = tmp_num + len(s)
                if strs[tmp_num:tmp_num + 1].lower() not in smlist:
                    strs = strs[:tmp_num - 1] + strs[tmp_num - 1:tmp_num].upper() + strs[tmp_num:]

    return strs


def onep(strs):
    restr = ''
    strs = sm(strs)
    for s in strs:
        if 'A' <= s and s <= 'Z':
            restr = restr + ' ' + s
        else:
            restr = restr + s

    restr = restr[1:]
    restr = restr.lower()
    return restr.split(' ')


def quanp2shuangp(quanpin):
    syllablelist = onep(sm(quanpin))
    return syllablelist


def py2hz(syllablelist):
    """
    用 Pinyin2Hanzi 库将音节列表识别为汉语词组，汉字可辅助校验全拼音节划分是否正确
    """
    result = viterbi(hmm_params=hmmparams, observations=(syllablelist), path_num=1, log=True)
    for item in result:
        phrase = ''.join(item.path)
        # print(phrase)
        # print(item.score, '/'.join(item.path))

    return phrase


if __name__ == "__main__":
    quanpin = 'yanwenzi'
    l = quanp2shuangp(quanpin)
    phrase = py2hz(l)
    print(quanpin + '\t拆分并识别为\t' + phrase)
    pass
