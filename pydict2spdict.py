import os

import pychaifen
import re
import pychaifen
from Pinyin2Hanzi import simplify_pinyin, is_pinyin
from pyshuangpin import *
from pypinyin import style, NORMAL


def pyd2spd(input_filename):
    """
    将 all_output_result_pinyin.txt 导出双拼版本
    """

    print(20 * '-')
    detail = False
    enable_detail = input('转换后是否包含全拼和汉字信息?y/n')
    if enable_detail == 'y':
        detail = True
        print('已启用，可能耗时较长')
    else:
        print('未启用')
    print(20 * '-')

    # 双拼方案选择
    print(20 * '-')
    shuangpin_type = int(input('1.小鹤\t2.自然码\t3.搜狗\t4.微软\t5.智能ABC\n选择一个方案：'))
    if shuangpin_type == 1:
        scheme = Scheme.小鹤
        print("已选择【小鹤】")
    elif shuangpin_type == 2:
        scheme = Scheme.自然码
        print("已选择【自然码】")
    elif shuangpin_type == 3:
        scheme = Scheme.搜狗
        print("已选择【搜狗】")
    elif shuangpin_type == 4:
        scheme = Scheme.微软
        print("已选择【微软】")
    elif shuangpin_type == 5:
        scheme = Scheme.智能ABC
        print("已选择【智能ABC】")
    else:
        print('请输入正确的序号！')
        exit()
    input('按回车确认...')
    print(20 * '-')
    print('等待转换...')

    # rime词库规定某些前缀无法作为开头需要删除
    def remove_prefix(text, prefix):
        while text.startswith(prefix):
            text = text[len(prefix):]
        return text

    # 读取文本文件
    with open(input_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    pattern = r'^(.*?)\t(.*)\t(.*)$'
    output_result_shuangpin = []
    output_result_shuangpin_bad = []

    # 遍历每一行并进行匹配
    for line in lines:
        if pattern:
            match = re.search(pattern, line)
            quanpin_text = match.group(2)  # 提取拼音
            syllablelist = pychaifen.quanp2shuangp(quanpin_text)

            # 检查编码是否为纯拼音编码
            is_pinyin_syllablelist = True
            for i in range(len(syllablelist)):
                syllable = syllablelist[i]
                # for syllable in syllablelist:
                if not is_pinyin(syllable):
                    syllable_mod = simplify_pinyin(syllable)
                    if not is_pinyin(syllable_mod):
                        is_pinyin_syllablelist = False
                        continue
                    else:
                        if syllable_mod != syllable:
                            syllablelist[i] = syllable_mod

            if is_pinyin_syllablelist:
                emoticon = remove_prefix(remove_prefix(match.group(1).strip(), "---"), "...")  # 提取颜文字表情,同时排除非法开头
                # 使用pyshuangpin库将全拼转换为双拼，支持小鹤、自然码、搜狗、微软、智能 ABC
                shuangpin_text = shuangpin_by_syllabl(syllablelist, scheme, style=NORMAL)
                shuangpin_str = ''.join([item[0] for item in shuangpin_text])
                # 格式化并写入到结果列表
                if detail:
                    hanzi_text = pychaifen.py2hz(syllablelist)
                    output_line = f"{emoticon}\t{shuangpin_str}\t1\t{quanpin_text}\t{hanzi_text}\n"  # 包含全拼和汉字信息
                else:
                    output_line = f"{emoticon}\t{shuangpin_str}\t1\n"
                output_result_shuangpin.append(output_line)
            else:
                # print('不是合法拼音:\t' + quanpin_text)
                emoticon = remove_prefix(remove_prefix(match.group(1).strip(), "---"), "...")  # 提取颜文字表情,同时排除非法开头
                # 格式化并写入到结果列表
                output_line = f"{emoticon}\t{quanpin_text}\t1\n"
                output_result_shuangpin_bad.append(output_line)

    return output_result_shuangpin, output_result_shuangpin_bad


if __name__ == "__main__":
    input_filename = 'data/all_output_result_pinyin.txt'

    # 词典转化
    output_result_shuangpin, output_result_shuangpin_bad = pyd2spd(input_filename)

    print(len(output_result_shuangpin), len(output_result_shuangpin_bad))

    output_filename = 'data/all_output_result_shuangpin.txt'
    output_filename2 = 'data/all_output_result_shuangpin_bad.txt'

    # 保存结果到文件
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        if output_result_shuangpin:
            output_file.writelines(output_result_shuangpin)
    print(f"结果已保存到{output_filename}文件中")

    # 保存结果到文件
    with open(output_filename2, 'w', encoding='utf-8') as output_file:
        if output_result_shuangpin_bad:
            output_file.writelines(output_result_shuangpin_bad)
    print(f"结果已保存到{output_filename2}文件中，请手动处理该文件")
