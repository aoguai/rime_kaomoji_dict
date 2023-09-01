import re
from pypinyin import pinyin, Style


def process_and_save_combined_kaomoji(input_filename, output_filename, is_pinyin=True, save_file=True):
    """
    处理并保存合并后的颜文字表情

    :param input_filename: 输入文件名
    :param output_filename: 输出文件名
    :param is_pinyin: 是否以拼音保存
    :param save_file: 是否保存到文件

    :return: 保存到文件的结果列表
    """

    # rime词库规定某些前缀无法作为开头需要删除
    def remove_prefix(text, prefix):
        while text.startswith(prefix):
            text = text[len(prefix):]
        return text

    # 读取文本文件
    with open(input_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    pattern = None
    chinese_english_pattern = None
    # 定义正则表达式模式
    if 'lmeee' in input_filename:
        pattern = r'<p>(.*?)<\/p><span class="copyBtn".*?data-desc="(.*?)".*?data-clipboard-text=".*?">.*?<\/span>'
        chinese_english_pattern = r'^[a-zA-Z\u4e00-\u9fa5]+$'
    elif 'Temreg' in input_filename:
        pattern = r'^(.*?)\t(.*)\t(.*)$'
    elif 'A_kaomoji' in input_filename:
        pattern = None
    elif 'custom_phrase' in input_filename:
        pattern = r'^(.*?)    (.*)$'
    elif 'sougou' in input_filename:
        pattern = r'<div class="ywz_content">(.*?)<\/div>.*?<div class="ywz_cont_name">输入文字：(.*?)<\/div>'
        chinese_english_pattern = r'^[a-zA-Z\u4e00-\u9fa5]+$'

    output_result_pinyin = []
    output_result_kmj = []

    # 遍历每一行并进行匹配
    for line in lines:
        if pattern:
            match = re.search(pattern, line)
            if match:
                if 'lmeee' in input_filename or 'sougou' in input_filename:
                    emoticon = remove_prefix(remove_prefix(match.group(1).strip(), "---"), "...")  # 提取颜文字表情,同时排除非法开头
                    chinese_text = match.group(2)  # 提取对应的中文
                    if is_pinyin:
                        # 去除空格后，检查中文或英文字符是否占据整个字符串
                        if re.match(chinese_english_pattern, chinese_text.replace(" ", "")):
                            # 使用PyPinyin库将中文转换为拼音
                            pinyin_text = pinyin(chinese_text, style=Style.NORMAL, heteronym=False)
                            pinyin_str = ''.join([item[0] for item in pinyin_text])

                            # 格式化并写入到结果列表
                            output_line = f"{emoticon}\t{pinyin_str}\t1\n"
                            output_result_pinyin.append(output_line)
                        else:
                            continue
                    else:
                        output_line = f"{emoticon}\tkmj\t1\n"
                        output_result_kmj.append(output_line)
                elif 'Temreg' in input_filename:
                    chinese_text = match.group(2)  # 提取拼音
                    emoticon = remove_prefix(remove_prefix(match.group(1).strip(), "---"), "...")  # 提取颜文字表情,同时排除非法开头
                    if is_pinyin:
                        # 格式化并写入到结果列表
                        output_line = f"{emoticon}\t{chinese_text}\t1\n"
                        output_result_pinyin.append(output_line)
                    else:
                        output_line = f"{emoticon}\tkmj\t1\n"
                        output_result_kmj.append(output_line)
                elif 'custom_phrase' in input_filename:
                    emoticon = remove_prefix(remove_prefix(match.group(2).strip(), "---"), "...")  # 提取颜文字表情,同时排除非法开头
                    chinese_text = match.group(1)  # 提取拼音
                    if is_pinyin:
                        # 格式化并写入到结果列表
                        output_line = f"{emoticon}\t{chinese_text}\t1\n"
                        output_result_pinyin.append(output_line)
                    else:
                        output_line = f"{emoticon}\tkmj\t1\n"
                        output_result_kmj.append(output_line)
        elif 'A_kaomoji' in input_filename:
            emoticon = remove_prefix(remove_prefix(line.strip(), "---"), "...")  # 提取颜文字表情,同时排除非法开头
            output_line = f"{emoticon}\tkmj\t1\n"
            output_result_kmj.append(output_line)

    # 保存结果到文件
    if save_file:
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            if is_pinyin:
                if 'A_kaomoji' in input_filename:
                    raise ValueError("A_kaomoji does not support pinyin conversion.")
                if output_result_pinyin:
                    output_file.writelines(output_result_pinyin)
            else:
                if output_result_kmj:
                    output_file.writelines(output_result_kmj)
        print(f"结果已保存到{output_filename}文件中")

    return output_result_pinyin, output_result_kmj


if __name__ == "__main__":

    def get_pinyin_key(item):
        parts = item.split("\t")
        chinese_pinyin = parts[1]
        return chinese_pinyin.lower()  # 转换为小写进行来忽略大小写


    all_output_result_pinyin = []
    all_output_result_kmj = []

    input_filename_list = ['data/A_kaomoji_dict_data.txt', 'data/custom_phrase_dict_data.txt',
                           'data/lmeee_dict_data.txt', 'data/sougou_dict_data.txt', 'data/Temreg_dict_data.txt']

    for input_filename in input_filename_list:
        output_result_pinyin, output_result_kmj = process_and_save_combined_kaomoji(input_filename=input_filename,
                                                                                    output_filename=input_filename.replace(
                                                                                        '.txt', '_output_file.txt'),
                                                                                    is_pinyin=False, save_file=False)
        all_output_result_pinyin.extend(output_result_pinyin)
        all_output_result_kmj.extend(output_result_kmj)
        if not 'A_kaomoji' in input_filename:
            output_result_pinyin, output_result_kmj = process_and_save_combined_kaomoji(input_filename=input_filename,
                                                                                        output_filename=input_filename.replace(
                                                                                            '.txt', '_output_file.txt'),
                                                                                        is_pinyin=True, save_file=False)
            all_output_result_pinyin.extend(output_result_pinyin)
            all_output_result_kmj.extend(output_result_kmj)

    # 使用集合进行去重
    all_output_result_pinyin = list(set(all_output_result_pinyin))
    all_output_result_kmj = list(set(all_output_result_kmj))

    # 排序
    all_output_result_pinyin = sorted(all_output_result_pinyin, key=get_pinyin_key)
    all_output_result_kmj = sorted(all_output_result_kmj, key=get_pinyin_key)

    print(len(all_output_result_pinyin), len(all_output_result_kmj))

    with open('data/all_output_result_pinyin.txt', 'w', encoding='utf-8') as output_file:
        output_file.writelines(all_output_result_pinyin)
        print(f"拼音字典结果已保存到data/all_output_result_pinyin.txt文件中")

    with open('data/all_output_result_kmj.txt', 'w', encoding='utf-8') as output_file:
        output_file.writelines(all_output_result_kmj)
        print(f"kmj字典结果已保存到data/all_output_result_kmj.txt文件中")