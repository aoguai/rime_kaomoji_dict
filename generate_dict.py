#!/usr/bin/env python3
"""
Rime颜文字词库生成工具

主要功能：
1. 从多种数据源生成颜文字词库
2. 支持生成全拼和双拼词库
3. 解决OpenCC空格问题和emoji撞车问题
4. 支持多种双拼方案
5. 自动去重排序功能，确保词库质量

使用方法:
    python generate_dict.py [options]

选项:
    --output-dir DIR       指定输出目录
    --all                  生成所有类型的词库(全拼词库、kmj词库和所有双拼方案词库)
    --pinyin               生成拼音版词库
    --kmj                  生成kmj版词库
    --shuangpin            生成双拼版词库
    --scheme {xiaohe,ziranma,sogou,microsoft,znabc}
                          指定双拼方案
    --no-special-space    不使用特殊空格替换普通空格
    --no-dedup            不对生成的词库进行去重
    --help                显示帮助信息
"""

import os
import re
import argparse
import datetime
from typing import List, Tuple, Dict
from pypinyin import NORMAL
from pyshuangpin import Scheme, shuangpin_by_syllabl

from kaomoji_processor import KaomojiProcessor


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='Rime颜文字词库生成工具')
    parser.add_argument('--output-dir', type=str, default='output',
                        help='指定输出目录 (默认: output)')
    parser.add_argument('--all', action='store_true',
                        help='生成所有类型的词库(全拼词库、kmj词库和所有双拼方案词库)')
    parser.add_argument('--pinyin', action='store_true',
                        help='生成拼音版词库')
    parser.add_argument('--kmj', action='store_true',
                        help='生成kmj版词库')
    parser.add_argument('--shuangpin', action='store_true',
                        help='生成双拼版词库')
    parser.add_argument('--scheme', type=str, choices=['xiaohe', 'ziranma', 'sogou', 'microsoft', 'znabc'],
                        default='xiaohe', help='指定双拼方案 (默认: xiaohe)')
    parser.add_argument('--no-special-space', action='store_true',
                        help='不使用特殊空格替换普通空格')
    parser.add_argument('--no-dedup', action='store_true',
                        help='不对生成的词库进行去重')
    return parser.parse_args()


def select_scheme(scheme_name: str) -> Scheme:
    """
    根据方案名称选择对应的双拼方案
    
    Args:
        scheme_name: 方案名称
        
    Returns:
        对应的Scheme枚举值
    """
    scheme_map = {
        'xiaohe': Scheme.小鹤,
        'ziranma': Scheme.自然码,
        'sogou': Scheme.搜狗,
        'microsoft': Scheme.微软,
        'znabc': Scheme.智能ABC
    }
    
    return scheme_map.get(scheme_name.lower(), Scheme.小鹤)


def get_all_schemes() -> Dict[str, Scheme]:
    """
    获取所有支持的双拼方案
    
    Returns:
        方案名称到Scheme枚举值的映射
    """
    return {
        'xiaohe': Scheme.小鹤,
        'ziranma': Scheme.自然码,
        'sogou': Scheme.搜狗,
        'microsoft': Scheme.微软,
        'znabc': Scheme.智能ABC
    }


def get_pinyin_key(item: str) -> str:
    """
    获取拼音键用于排序
    
    Args:
        item: 包含拼音的行
        
    Returns:
        拼音键(小写)
    """
    parts = item.split("\t")
    if len(parts) > 1:
        chinese_pinyin = parts[1]
        return chinese_pinyin.lower()  # 转换为小写进行来忽略大小写
    return ""


def dedup_and_sort(lines: List[str], sort_key_func=None) -> List[str]:
    """
    去除重复行并排序
    
    Args:
        lines: 需要去重排序的行列表
        sort_key_func: 排序键函数，默认使用get_pinyin_key
        
    Returns:
        去重排序后的行列表
    """
    # 去除重复的行
    unique_lines = list(set(lines))
    
    # 排序
    if sort_key_func:
        sorted_lines = sorted(unique_lines, key=sort_key_func)
    else:
        sorted_lines = sorted(unique_lines, key=get_pinyin_key)
        
    return sorted_lines


def generate_pinyin_dictionary(processor: KaomojiProcessor, 
                              input_files: List[str], 
                              output_file: str,
                              use_special_space: bool = True,
                              use_dedup: bool = True) -> List[str]:
    """
    生成拼音版词库
    
    Args:
        processor: 颜文字处理器
        input_files: 输入文件列表
        output_file: 输出文件路径
        use_special_space: 是否使用特殊空格
        use_dedup: 是否进行去重排序
        
    Returns:
        处理结果列表
    """
    all_output_result = []
    
    print("正在生成拼音版词库...")
    for input_filename in input_files:
        if not os.path.exists(input_filename):
            print(f"警告: 文件 {input_filename} 不存在，已跳过")
            continue
            
        # A_kaomoji文件不支持拼音转换，直接跳过
        if 'A_kaomoji' in input_filename:
            continue
            
        pinyin_results, _ = processor.process_file(
            input_filename=input_filename,
            is_pinyin=True,
            save_file=False,
            use_special_space=use_special_space
        )
        all_output_result.extend(pinyin_results)
    
    # 使用去重排序函数处理结果
    if use_dedup:
        all_output_result = dedup_and_sort(all_output_result)
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as output_file_obj:
        output_file_obj.writelines(all_output_result)
    
    print(f"拼音版词库已生成，共 {len(all_output_result)} 个颜文字")
    return all_output_result


def generate_kmj_dictionary(processor: KaomojiProcessor, 
                           input_files: List[str], 
                           output_file: str,
                           use_special_space: bool = True,
                           use_dedup: bool = True) -> List[str]:
    """
    生成kmj版词库
    
    Args:
        processor: 颜文字处理器
        input_files: 输入文件列表
        output_file: 输出文件路径
        use_special_space: 是否使用特殊空格
        use_dedup: 是否进行去重排序
        
    Returns:
        处理结果列表
    """
    all_output_result = []
    
    print("正在生成kmj版词库...")
    for input_filename in input_files:
        if not os.path.exists(input_filename):
            print(f"警告: 文件 {input_filename} 不存在，已跳过")
            continue
            
        _, kmj_results = processor.process_file(
            input_filename=input_filename,
            is_pinyin=False,
            save_file=False,
            use_special_space=use_special_space
        )
        all_output_result.extend(kmj_results)
    
    # 使用去重排序函数处理结果
    if use_dedup:
        all_output_result = dedup_and_sort(all_output_result)
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as output_file_obj:
        output_file_obj.writelines(all_output_result)
    
    print(f"kmj版词库已生成，共 {len(all_output_result)} 个颜文字")
    return all_output_result


def generate_shuangpin_dictionary(pinyin_dict_file: str, 
                                 output_file: str,
                                 scheme: Scheme,
                                 include_details: bool = False,
                                 use_dedup: bool = True,
                                 use_special_space: bool = True) -> Tuple[List[str], List[str]]:
    """
    生成双拼版词库
    
    Args:
        pinyin_dict_file: 拼音词库文件路径
        output_file: 输出文件路径
        scheme: 双拼方案
        include_details: 是否包含详细信息(全拼和汉字)
        use_dedup: 是否进行去重排序
        use_special_space: 是否使用特殊空格(U+2002)
        
    Returns:
        处理结果元组 (成功列表, 失败列表)
    """
    from Pinyin2Hanzi import simplify_pinyin, is_pinyin
    import pychaifen
    
    if not os.path.exists(pinyin_dict_file):
        print(f"错误: 拼音词库文件 {pinyin_dict_file} 不存在")
        return [], []
        
    print(f"正在生成双拼版词库 (方案: {scheme.name})...")
    
    # 读取拼音词库
    with open(pinyin_dict_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    pattern = r'^(.*?)\t(.*)\t(.*)$'
    output_result_shuangpin = []
    output_result_shuangpin_bad = []  # 仅用于记录完全无法处理的条目
    
    # 处理每一行
    for line in lines:
        match = re.search(pattern, line)
        if match:
            quanpin_text = match.group(2)  # 提取拼音
            emoticon = match.group(1).strip()  # 提取颜文字
            
            # 处理任何类型的空格，包括普通空格和特殊空格
            space_char = '\u2002' if use_special_space else ' '
            
            # 检测并替换特殊空格为临时标记，以便后续处理
            has_special_spaces = '\u2002' in quanpin_text
            if has_special_spaces:
                # 临时替换特殊空格为普通空格进行处理
                temp_quanpin_text = quanpin_text.replace('\u2002', ' ')
            else:
                temp_quanpin_text = quanpin_text
                
            # 处理带空格的拼音情况
            if ' ' in temp_quanpin_text or has_special_spaces:
                # 按空格分割拼音字符串
                quanpin_parts = temp_quanpin_text.split(' ')
                shuangpin_parts = []
                
                # 逐个处理每部分拼音
                for part in quanpin_parts:
                    if not part:  # 跳过空字符串
                        continue
                        
                    syllablelist = pychaifen.quanp2shuangp(part)
                    
                    # 检查编码是否为纯拼音编码
                    is_pinyin_syllablelist = True
                    for i in range(len(syllablelist)):
                        syllable = syllablelist[i]
                        if not is_pinyin(syllable):
                            syllable_mod = simplify_pinyin(syllable)
                            if not is_pinyin(syllable_mod):
                                is_pinyin_syllablelist = False
                                continue
                            else:
                                if syllable_mod != syllable:
                                    syllablelist[i] = syllable_mod
                    
                    if is_pinyin_syllablelist:
                        # 使用pyshuangpin库将全拼转换为双拼
                        shuangpin_text = shuangpin_by_syllabl(syllablelist, scheme, style=NORMAL)
                        shuangpin_str = ''.join([item[0] for item in shuangpin_text])
                        shuangpin_parts.append(shuangpin_str)
                    else:
                        # 对于无效的拼音部分，保留原始文本
                        shuangpin_parts.append(part)
                
                # 用适当的空格类型重新连接各部分双拼结果
                final_shuangpin_str = space_char.join(shuangpin_parts)
                
                # 格式化输出行
                if include_details:
                    output_line = f"{emoticon}\t{final_shuangpin_str}\t1\t{quanpin_text}\n"
                else:
                    output_line = f"{emoticon}\t{final_shuangpin_str}\t1\n"
                    
                output_result_shuangpin.append(output_line)
            else:
                # 无空格情况
                syllablelist = pychaifen.quanp2shuangp(quanpin_text)
                
                # 检查编码是否为纯拼音编码
                is_pinyin_syllablelist = True
                for i in range(len(syllablelist)):
                    syllable = syllablelist[i]
                    if not is_pinyin(syllable):
                        syllable_mod = simplify_pinyin(syllable)
                        if not is_pinyin(syllable_mod):
                            is_pinyin_syllablelist = False
                            continue
                        else:
                            if syllable_mod != syllable:
                                syllablelist[i] = syllable_mod
                
                if is_pinyin_syllablelist:
                    # 使用pyshuangpin库将全拼转换为双拼
                    shuangpin_text = shuangpin_by_syllabl(syllablelist, scheme, style=NORMAL)
                    shuangpin_str = ''.join([item[0] for item in shuangpin_text])
                    
                    # 格式化输出行
                    if include_details:
                        hanzi_text = pychaifen.py2hz(syllablelist)
                        output_line = f"{emoticon}\t{shuangpin_str}\t1\t{quanpin_text}\t{hanzi_text}\n"
                    else:
                        output_line = f"{emoticon}\t{shuangpin_str}\t1\n"
                        
                    output_result_shuangpin.append(output_line)
                else:
                    # 对于单字母或中文缩写等，直接使用原始文本作为双拼结果
                    output_line = f"{emoticon}\t{quanpin_text}\t1\n"
                    output_result_shuangpin.append(output_line)
        else:
            # 不符合格式的行添加到bad结果
            output_result_shuangpin_bad.append(line)
    
    # 如果启用去重，对结果进行去重排序
    if use_dedup:
        output_result_shuangpin = dedup_and_sort(output_result_shuangpin)
        output_result_shuangpin_bad = dedup_and_sort(output_result_shuangpin_bad)
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as output_file_obj:
        output_file_obj.writelines(output_result_shuangpin)
        
    # 保存格式不符的结果
    if output_result_shuangpin_bad:
        bad_output_file = output_file.replace('.txt', '_format_error.txt')
        with open(bad_output_file, 'w', encoding='utf-8') as output_file_obj:
            output_file_obj.writelines(output_result_shuangpin_bad)
        print(f"格式可能错误条目已保存到: {bad_output_file}")
        
    print(f"双拼版词库已生成，共 {len(output_result_shuangpin)} 个有效条目，{len(output_result_shuangpin_bad)} 个格式可能错误条目")
    return output_result_shuangpin, output_result_shuangpin_bad


def generate_rime_dict_file(input_file: str, output_file: str, dict_name: str, dict_type: str):
    """
    生成Rime词库文件(.dict.yaml)
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
        dict_name: 词库名称
        dict_type: 词库类型
    """
    if not os.path.exists(input_file):
        print(f"错误: 输入文件 {input_file} 不存在")
        return
        
    # 读取词条
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # 统计词条数量
    entry_count = content.count('\n')
    
    # 获取当前日期，格式为YYYY-MM-DD
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 生成词库头部
    header = f"""# Rime dictionary
# encoding: utf-8
#
# Kaomoji dictionary for Rime input method engine
# 
# Created with rime_kaomoji_dict generator
#
# https://github.com/aoguai/rime_kaomoji_dict

---
name: {dict_name}
version: "{current_date}"
sort: by_weight
use_preset_vocabulary: false
max_phrase_length: 99
min_phrase_weight: 1
...

# {dict_type} entries: {entry_count}
"""
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # 写入词库文件
    with open(output_file, 'w', encoding='utf-8') as output_file_obj:
        output_file_obj.write(header + content)
        
    print(f"已生成Rime词库文件: {output_file}")


def main():
    """主函数"""
    args = parse_arguments()
    
    # 如果没有指定任何操作，默认生成所有类型词库
    if not (args.all or args.pinyin or args.kmj or args.shuangpin):
        args.all = True
        
    # 初始化颜文字处理器
    processor = KaomojiProcessor()
    
    # 输入文件列表
    input_files = [
        'data/A_kaomoji_dict_data.txt',
        'data/custom_phrase_dict_data.txt',
        'data/lmeee_dict_data.txt',
        'data/sougou_dict_data.txt',
        'data/Temreg_dict_data.txt'
    ]
    
    # 确保输出目录存在
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 使用特殊空格
    use_special_space = not args.no_special_space
    
    # 是否使用去重
    use_dedup = not args.no_dedup
    
    # 临时文件路径
    pinyin_txt_file = os.path.join(args.output_dir, 'all_output_result_pinyin.txt')
    kmj_txt_file = os.path.join(args.output_dir, 'all_output_result_kmj.txt')
    
    # 生成拼音版词库(--all或--pinyin或--shuangpin选项)
    if args.all or args.pinyin or args.shuangpin:
        pinyin_results = generate_pinyin_dictionary(
            processor, input_files, pinyin_txt_file, 
            use_special_space=use_special_space,
            use_dedup=use_dedup
        )
        generate_rime_dict_file(
            pinyin_txt_file, 
            os.path.join(args.output_dir, 'kaomoji_pinyin.dict.yaml'), 
            'kaomoji_pinyin', 
            'Pinyin'
        )
        
    # 生成kmj版词库(--all或--kmj选项)
    if args.all or args.kmj:
        kmj_results = generate_kmj_dictionary(
            processor, input_files, kmj_txt_file, 
            use_special_space=use_special_space,
            use_dedup=use_dedup
        )
        generate_rime_dict_file(
            kmj_txt_file, 
            os.path.join(args.output_dir, 'kaomoji_kmj.dict.yaml'), 
            'kaomoji_kmj', 
            'KMJ'
        )
        
    # 生成双拼版词库(--all选项生成所有方案，--shuangpin选项生成指定方案)
    if args.all:
        # 生成所有双拼方案的词库
        all_schemes = get_all_schemes()
        for scheme_name, scheme in all_schemes.items():
            shuangpin_txt_file = os.path.join(args.output_dir, f'all_output_result_shuangpin_{scheme_name}.txt')
            shuangpin_dict_file = os.path.join(args.output_dir, f'kaomoji_shuangpin_{scheme_name}.dict.yaml')
            
            # 确保拼音词库已生成
            if not os.path.exists(pinyin_txt_file):
                print(f"错误: 拼音词库文件 {pinyin_txt_file} 不存在，无法生成双拼词库")
                continue
                
            shuangpin_results, shuangpin_bad_results = generate_shuangpin_dictionary(
                pinyin_txt_file, shuangpin_txt_file, scheme, 
                include_details=False,
                use_dedup=use_dedup,
                use_special_space=use_special_space
            )
            generate_rime_dict_file(
                shuangpin_txt_file, 
                shuangpin_dict_file, 
                f'kaomoji_shuangpin_{scheme_name}', 
                f'Shuangpin ({scheme_name})'
            )
    elif args.shuangpin:
        # 只生成指定方案的双拼词库
        scheme = select_scheme(args.scheme)
        shuangpin_txt_file = os.path.join(args.output_dir, f'all_output_result_shuangpin_{args.scheme}.txt')
        shuangpin_dict_file = os.path.join(args.output_dir, f'kaomoji_shuangpin_{args.scheme}.dict.yaml')
        
        shuangpin_results, shuangpin_bad_results = generate_shuangpin_dictionary(
            pinyin_txt_file, shuangpin_txt_file, scheme, 
            include_details=False,
            use_dedup=use_dedup,
            use_special_space=use_special_space
        )
        generate_rime_dict_file(
            shuangpin_txt_file, 
            shuangpin_dict_file, 
            f'kaomoji_shuangpin_{args.scheme}', 
            f'Shuangpin ({args.scheme})'
        )
    
    print("词库生成完成!")
    print(f"输出目录: {os.path.abspath(args.output_dir)}")


if __name__ == "__main__":
    main() 