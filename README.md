# rime_kaomoji_dict

一个颜文字 (kaomoji) 词库，同时可以生成适用于 [Rime 输入法](https://rime.im/) 的词库。

A collection of kaomoji expressions, also capable of generating dictionaries suitable for the [Rime input method](https://rime.im/).

## 目录结构

以下是对主要目录结构的说明:

```
rime_kaomoji_dict
├─ data
│    ├─ A_kaomoji_dict_data.txt：A岛匿名版部分颜文字素材（无编码信息）
│    ├─ Temreg_dict_data.txt：百度贴吧吧友Temreg分享的颜文字素材
│    ├─ custom_phrase_dict_data.txt： girhub kaos 项目中的颜文字素材
│    ├─ lmeee_dict_data.txt：拉米工具颜文字素材
│    └─ sougou_dict_data.txt：搜狗颜文字与A岛匿名版部分颜文字（有编码信息）素材
├─ kaomoji_processor.py：颜文字处理核心模块
├─ generate_dict.py：一站式词库生成工具
└─ test_display.py：颜文字特殊空格显示测试脚本
```

## 特性与解决方案

这个工具尝试解决了两个主要问题：

1. **OpenCC空格处理问题**：用特殊空格(U+2002)替换普通空格(U+0020)，尝试解决了OpenCC将空格作为分隔符导致的颜文字分割问题。

2. **Emoji撞车问题**：使用统一的`kmj`标记为颜文字添加特定标识，与emoji区分开来，不会相互干扰。

## 安装与使用

本项目不仅可以用于生成适用于 [Rime 输入法](https://rime.im/) 的词库，也可以用于生成其他输入法的词库。

同时您还可以将其视为一般颜文字词库，用于网络表情NLP，颜文字识别，颜文字表情实体识别、属性检测、新颜发现等。

### 安装依赖

```bash
pip install -r requirements.txt
```

### 生成词库

项目提供了一站式词库生成工具`generate_dict.py`，支持多种选项：

```bash
python generate_dict.py [options]
```

选项说明：

```
--output-dir DIR       指定输出目录 (默认: output)
--all                  生成所有类型的词库(全拼词库、kmj词库和所有双拼方案词库)
--pinyin               生成拼音版词库
--kmj                  生成kmj版词库
--shuangpin            生成双拼版词库
--scheme {xiaohe,ziranma,sogou,microsoft,znabc}
                       指定双拼方案 (默认: xiaohe)
--no-special-space     不使用特殊空格替换普通空格
--no-dedup             不对生成的词库进行去重
--help                 显示帮助信息
```

例如，生成全拼和小鹤双拼词库：

```bash
python generate_dict.py --pinyin --shuangpin --scheme xiaohe
```

生成所有类型词库（包括全拼、kmj和所有双拼方案）：

```bash
python generate_dict.py --all
```

生成指定双拼方案的词库：

```bash
python generate_dict.py --shuangpin --scheme sogou
```

默认情况下，如果不指定任何选项，会生成所有类型的词库（等同于使用--all选项）。

### 直接使用预生成的词库

如果您没有开发需求，可以直接前往 [releases](https://github.com/aoguai/rime_kaomoji_dict/releases) 下载最新版本的词库文件，直接使用即可。

解压后你会得到以下适用于Rime输入法的词库文件:
```
kaomoji_pinyin.dict.yaml            # 全拼版颜文字词库
kaomoji_kmj.dict.yaml               # kmj标记版颜文字词库
kaomoji_shuangpin_xiaohe.dict.yaml  # 小鹤双拼版颜文字词库
kaomoji_shuangpin_ziranma.dict.yaml # 自然码双拼版颜文字词库
kaomoji_shuangpin_sogou.dict.yaml   # 搜狗双拼版颜文字词库
kaomoji_shuangpin_microsoft.dict.yaml # 微软双拼版颜文字词库
kaomoji_shuangpin_znabc.dict.yaml   # 智能ABC双拼版颜文字词库
```

它们的区别在于：

- `kaomoji_kmj.dict.yaml`：固定将**所有颜文字**的**编码**设置为`kmj`
- `kaomoji_pinyin.dict.yaml`：使用颜文字对应中文的拼音作为编码
- `kaomoji_shuangpin_*.dict.yaml`：使用不同双拼方案对应的编码

### 词库差异与选择

不同类型词库的实际输入体验：

- **全拼版**：输入颜文字对应中文的拼音，如输入`kaixin`可能得到`(✿◡‿◡)`
- **kmj版**：输入`kmj`获取所有颜文字，可结合Rime的模糊搜索功能
- **双拼版**：输入颜文字对应中文的双拼编码，如小鹤双拼输入`kx`可能得到`(✿◡‿◡)`

您可以根据自己的喜好和输入习惯选择适合的词库。不同词库之间不冲突，可以同时启用多个。

## 项目技术说明

### 空格处理方案

项目使用Unicode En空格(U+2002)替换普通空格(U+0020)来解决OpenCC的分词问题。此特殊空格在几乎所有平台和字体中都能正常显示，与普通空格视觉效果基本一致。

### 自定义构建

如果您需要自定义处理逻辑，可以直接修改`kaomoji_processor.py`：

- `replace_spaces`方法：控制空格替换逻辑
- `process_kaomoji`方法：颜文字整体处理逻辑
- `process_source_data`方法：数据源处理逻辑

### 生成双拼词库

从本仓库源码构建双拼词库时，`generate_dict.py`会自动将全拼词库转换为指定的双拼方案。支持小鹤双拼、自然码、搜狗双拼、微软双拼、智能ABC双拼方案。

由于音节划分算法有局限，部分形如pingan的编码会取pin/gan而非ping/an导致转换不正确，这部分会被标记为转换失败并保存到单独的文件中。

### 去重排序功能

为了提高词库质量，所有类型的词库生成过程都会默认进行去重和排序处理。去重功能消除了来自不同数据源的重复颜文字条目，排序则按照拼音顺序对词库进行组织，提供更好的使用体验。

如果出于特殊原因需要保留重复条目，可以使用`--no-dedup`选项禁用去重功能。

## 数据原始来源

[X岛匿名版](https://www.nmbxd1.com/Forum)

[颜文字大全 - 拉米工具](https://tool.lmeee.com/yanwenzi)

[求助小狼毫怎么输入颜文字。【rime吧】_百度贴吧](https://tieba.baidu.com/p/2357282768)

[kaos/dict.txt at master · tisyang/kaos](https://github.com/tisyang/kaos/blob/master/dict.txt)

[搜狗颜文字](https://pinyin.sogou.com/dict/ywz/?f=dict_index&ytype=24)

### 贡献者们
感谢贡献者们对本项目作出的贡献:
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="100%"><a href="https://github.com/xtmu"><img src="https://avatars.githubusercontent.com/u/90405292?v=4?s=100" width="100px;" alt="Well404"/><br /><sub><b>xtmu</b></sub></a><br /><a href="https://github.com/aoguai/rime_kaomoji_dict/commits/shuangpin?author=xtmu" title="Code">💻</a></a><a href="https://github.com/aoguai/rime_kaomoji_dict//issues?q=author:xtmu" title="Bug reports">🐛</a></a><a href="https://github.com/aoguai/rime_kaomoji_dict/commits/shuangpin?author=xtmu" title="Bug reports">🚧</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## 免责声明
[rime_kaomoji_dict](https://github.com/aoguai/rime_kaomoji_dict) 遵循 [MIT 开源协议](https://github.com/aoguai/rime_kaomoji_dict/blob/master/LICENSE)。