def dedup(input_file_name):
    """
    去除文件中的重复条目并排序
    """

    output_file_name = input_file_name.replace('.txt', '_sorted.txt')

    # 打开要读取的文本文件，指定编码为UTF-8
    with open(input_file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 按照每行第一个制表符后面的单词首字母排序，忽略大小写
    def get_first_word_after_tab(line):
        parts = line.split('\t')
        if len(parts) > 1:
            return parts[1].strip()[0].lower()
        else:
            return ''

    # 去除重复的行
    unique_lines = list(set(lines))

    # 排序
    sorted_lines = sorted(unique_lines, key=get_first_word_after_tab)

    # 打开要写入的输出文件，指定编码为UTF-8
    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        # 将排序后的结果写入输出文件
        output_file.writelines(sorted_lines)

    print(len(lines), len(sorted_lines))
    print("排序完成并已写入" + output_file_name + "文件。")


if __name__ == "__main__":
    input_file_name = 'data/all_output_result_shuangpin.txt'
    dedup(input_file_name)
