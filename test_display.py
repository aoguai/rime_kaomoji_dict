#!/usr/bin/env python3
"""
颜文字特殊空格显示测试脚本

此脚本用于测试特殊空格(U+2002)在当前环境下的显示效果，
以确保处理后的颜文字能正常显示。
"""

import sys

def print_with_info(text, label):
    """打印字符串及其空格信息"""
    print(f"{label}: '{text}'")
    
    # 打印空格信息
    spaces_info = []
    for i, char in enumerate(text):
        if char.isspace():
            code_point = ord(char)
            name = space_name(code_point)
            spaces_info.append(f"位置 {i}: U+{code_point:04X} ({name})")
    
    if spaces_info:
        print("空格信息:")
        for info in spaces_info:
            print(f"  {info}")
    else:
        print("  无空格")
    print()

def space_name(code_point):
    """根据代码点返回空格名称"""
    if code_point == 0x0020:
        return "普通空格 SPACE"
    elif code_point == 0x2002:
        return "En空格 EN SPACE"
    elif code_point == 0x2003:
        return "Em空格 EM SPACE"
    elif code_point == 0x2004:
        return "三分之一Em空格 THREE-PER-EM SPACE"
    elif code_point == 0x2005:
        return "四分之一Em空格 FOUR-PER-EM SPACE"
    elif code_point == 0x2006:
        return "六分之一Em空格 SIX-PER-EM SPACE"
    elif code_point == 0x2007:
        return "数字空格 FIGURE SPACE"
    elif code_point == 0x2008:
        return "标点空格 PUNCTUATION SPACE"
    elif code_point == 0x2009:
        return "窄空格 THIN SPACE"
    elif code_point == 0x200A:
        return "发空格 HAIR SPACE"
    elif code_point == 0x200B:
        return "零宽空格 ZERO WIDTH SPACE"
    elif code_point == 0x00A0:
        return "不换行空格 NO-BREAK SPACE"
    elif code_point == 0x3000:
        return "表意文字空格 IDEOGRAPHIC SPACE"
    else:
        return f"未知空格 Unknown space character"

def main():
    """主函数"""
    print("颜文字特殊空格显示测试\n")
    
    # 测试颜文字样例
    test_cases = [
        ("普通空格", "( ﾟ∀ﾟ) ﾉ♡"),
        ("En空格", "(\u2002ﾟ∀ﾟ)\u2002ﾉ♡"),
        ("混合空格", "( ﾟ∀ﾟ)\u2002ﾉ♡"),
    ]
    
    # 打印系统信息
    print(f"Python版本: {sys.version}")
    print(f"系统编码: {sys.getdefaultencoding()}")
    print(f"控制台编码: {sys.stdout.encoding}\n")
    
    # 测试各种空格
    print("空格字符测试:")
    print(f"普通空格 (U+0020): ' '")
    print(f"En空格 (U+2002): '\u2002'")
    print(f"Em空格 (U+2003): '\u2003'")
    print(f"不换行空格 (U+00A0): '\u00A0'")
    print(f"表意文字空格 (U+3000): '\u3000'\n")
    
    # 测试颜文字
    print("颜文字样例测试:")
    for label, text in test_cases:
        print_with_info(text, label)

    # 自定义测试
    print("你可以输入自定义颜文字进行测试 (输入'q'退出):")
    while True:
        user_input = input("> ")
        if user_input.lower() == 'q':
            break
        print_with_info(user_input, "用户输入")

    # 替换测试
    print("\n空格替换测试:")
    test_text = "( ﾟ∀ﾟ) ﾉ♡"
    replaced_text = test_text.replace(' ', '\u2002')
    print_with_info(test_text, "原始文本")
    print_with_info(replaced_text, "替换后文本")
    
    # 结论
    print("\n测试结论:")
    print("1. 如果En空格(U+2002)能够正常显示，且视觉效果与普通空格相近，则颜文字处理正常")
    print("2. 特殊空格主要用于解决OpenCC分词问题，不会影响正常显示效果")

if __name__ == "__main__":
    main() 