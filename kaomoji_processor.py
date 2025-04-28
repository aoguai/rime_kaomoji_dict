"""
颜文字处理模块 - 处理颜文字相关操作

主要功能：
1. 空格替换：将普通空格替换为en空格(U+2002)，解决OpenCC分词问题
2. 颜文字标记：为颜文字添加特定标记，区分于emoji
3. 格式转换：将不同格式的颜文字数据转换为标准格式
"""

import re
from typing import List, Tuple
from pypinyin import pinyin, Style


class KaomojiProcessor:
    """
    颜文字处理类，提供颜文字相关的处理功能
    """
    
    def __init__(self):
        """初始化颜文字处理器"""
        # 禁止的前缀，Rime词库规定某些前缀无法作为开头需要删除
        self.invalid_prefixes = ["---", "..."]
        # 中文和英文字符的正则表达式
        self.chinese_english_pattern = r'^[a-zA-Z\u4e00-\u9fa5]+$'
        
    def replace_spaces(self, text: str) -> str:
        """
        将普通空格(U+0020)替换为en空格(U+2002)
        
        Args:
            text: 包含普通空格的文本
            
        Returns:
            替换空格后的文本
        """
        # 替换普通空格为en空格(U+2002)
        return text.replace(' ', '\u2002')
    
    def remove_invalid_prefixes(self, text: str) -> str:
        """
        移除无效的前缀
        
        Args:
            text: 需要处理的文本
            
        Returns:
            移除前缀后的文本
        """
        result = text.strip()
        for prefix in self.invalid_prefixes:
            while result.startswith(prefix):
                result = result[len(prefix):]
        return result
    
    def process_kaomoji(self, kaomoji: str, use_special_space: bool = True) -> str:
        """
        处理颜文字，移除无效前缀并可选择替换空格
        
        Args:
            kaomoji: 原始颜文字
            use_special_space: 是否使用特殊空格替换普通空格
            
        Returns:
            处理后的颜文字
        """
        result = self.remove_invalid_prefixes(kaomoji)
        if use_special_space:
            result = self.replace_spaces(result)
        return result
    
    def is_chinese_english_text(self, text: str) -> bool:
        """
        检查文本是否只包含中文和英文字符(去除空格后)
        
        Args:
            text: 需要检查的文本
            
        Returns:
            如果只包含中文和英文字符，返回True；否则返回False
        """
        return bool(re.match(self.chinese_english_pattern, text.replace(" ", "")))
    
    def get_pinyin_for_text(self, text: str) -> str:
        """
        获取文本的拼音
        
        Args:
            text: 需要转换的文本
            
        Returns:
            文本的拼音，以空格分隔
        """
        pinyin_result = pinyin(text, style=Style.NORMAL, heteronym=False)
        return ' '.join([item[0] for item in pinyin_result])
    
    def process_source_data(self, 
                           content: str, 
                           source_type: str, 
                           is_pinyin: bool = True, 
                           use_special_space: bool = True) -> Tuple[List[str], List[str]]:
        """
        处理源数据，从不同来源的数据中提取颜文字和对应的拼音或标记
        
        Args:
            content: 源数据内容
            source_type: 源数据类型（'lmeee', 'Temreg', 'A_kaomoji', 'custom_phrase', 'sougou'）
            is_pinyin: 是否以拼音格式保存
            use_special_space: 是否使用特殊空格替换普通空格
            
        Returns:
            包含处理结果的元组 (拼音结果列表, kmj结果列表)
        """
        output_result_pinyin = []
        output_result_kmj = []
        
        # 根据不同的数据源使用不同的正则表达式
        pattern = None
        chinese_english_pattern = None
        
        if 'lmeee' in source_type:
            pattern = r'<p>(.*?)<\/p><span class="copyBtn".*?data-desc="(.*?)".*?data-clipboard-text=".*?">.*?<\/span>'
            chinese_english_pattern = self.chinese_english_pattern
        elif 'Temreg' in source_type:
            pattern = r'^(.*?)\t(.*)\t(.*)$'
        elif 'A_kaomoji' in source_type:
            pattern = None
        elif 'custom_phrase' in source_type:
            pattern = r'^(.*?)    (.*)$'
        elif 'sougou' in source_type:
            pattern = r'<div class="ywz_content">(.*?)<\/div>.*?<div class="ywz_cont_name">输入文字：(.*?)<\/div>'
            chinese_english_pattern = self.chinese_english_pattern
        
        # 按行处理内容
        lines = content.splitlines()
        for line in lines:
            if pattern:
                match = re.search(pattern, line)
                if match:
                    if 'lmeee' in source_type or 'sougou' in source_type:
                        emoticon = self.process_kaomoji(match.group(1), use_special_space)
                        chinese_text = match.group(2)
                        if is_pinyin:
                            # 去除空格后，检查中文或英文字符是否占据整个字符串
                            if re.match(chinese_english_pattern, chinese_text.replace(" ", "")):
                                pinyin_str = self.get_pinyin_for_text(chinese_text)
                                output_line = f"{emoticon}\t{pinyin_str}\t0\n"
                                output_result_pinyin.append(output_line)
                            else:
                                continue
                        else:
                            output_line = f"{emoticon}\tkmj\t0\n"
                            output_result_kmj.append(output_line)
                    elif 'Temreg' in source_type:
                        chinese_text = match.group(2)  # 提取拼音
                        emoticon = self.process_kaomoji(match.group(1), use_special_space)
                        if is_pinyin:
                            output_line = f"{emoticon}\t{chinese_text}\t0\n"
                            output_result_pinyin.append(output_line)
                        else:
                            output_line = f"{emoticon}\tkmj\t0\n"
                            output_result_kmj.append(output_line)
                    elif 'custom_phrase' in source_type:
                        emoticon = self.process_kaomoji(match.group(2), use_special_space)
                        chinese_text = match.group(1)  # 提取拼音
                        if is_pinyin:
                            output_line = f"{emoticon}\t{chinese_text}\t0\n"
                            output_result_pinyin.append(output_line)
                        else:
                            output_line = f"{emoticon}\tkmj\t0\n"
                            output_result_kmj.append(output_line)
            elif 'A_kaomoji' in source_type:
                emoticon = self.process_kaomoji(line.strip(), use_special_space)
                output_line = f"{emoticon}\tkmj\t0\n"
                output_result_kmj.append(output_line)
                
        return output_result_pinyin, output_result_kmj
    
    def process_file(self, 
                    input_filename: str, 
                    output_filename: str = None,
                    is_pinyin: bool = True, 
                    save_file: bool = True,
                    use_special_space: bool = True) -> Tuple[List[str], List[str]]:
        """
        处理并保存颜文字文件
        
        Args:
            input_filename: 输入文件名
            output_filename: 输出文件名，如为None则不保存
            is_pinyin: 是否以拼音保存
            save_file: 是否保存到文件
            use_special_space: 是否使用特殊空格替换普通空格
            
        Returns:
            包含处理结果的元组 (拼音结果列表, kmj结果列表)
        """
        try:
            # 读取文本文件
            with open(input_filename, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # 处理源数据
            output_result_pinyin, output_result_kmj = self.process_source_data(
                content, input_filename, is_pinyin, use_special_space
            )
            
            # 保存结果到文件
            if save_file and output_filename:
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
            
        except Exception as e:
            print(f"处理文件 {input_filename} 时发生错误: {str(e)}")
            return [], []


if __name__ == "__main__":
    # 简单测试
    processor = KaomojiProcessor()
    test_kaomoji = "( ﾟ∀ﾟ) ﾉ♡"
    print(f"原始颜文字: '{test_kaomoji}'")
    processed = processor.process_kaomoji(test_kaomoji)
    print(f"处理后颜文字: '{processed}'")
    print(f"空格编码: {ord(' ')}, 处理后空格编码: {ord(processed[7])}") 