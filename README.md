# rime_kaomoji_dict

一个颜文字 (kaomoji) 词库，同时可以生成适用于 [Rime 输入法](https://rime.im/) 的词库。

A collection of kaomoji expressions, also capable of generating dictionaries suitable for the [Rime input method](https://rime.im/).

## 目录结构

以下是对主要目录结构的说明:

```html
rime_kaomoji_dict
├─ data
│    ├─ A_kaomoji_dict_data.txt：A岛匿名版部分颜文字素材（无编码信息）
│    ├─ Temreg_dict_data.txt：百度贴吧吧友Temreg分享的颜文字素材
│    ├─ custom_phrase_dict_data.txt： girhub kaos 项目中的颜文字素材
│    ├─ lmeee_dict_data.txt：拉米工具颜文字素材
│    └─ sougou_dict_data.txt：搜狗颜文字与A岛匿名版部分颜文字（有编码信息）素材
└─ main.py：处理颜文字素材的脚本
```
## 安装与使用
本项目不仅可以用于生成适用于 [Rime 输入法](https://rime.im/) 的词库，也可以用于生成其他输入法的词库。

同时您还可以将其视为一般颜文字词库，用于网络表情 NLP ，颜文字识别，颜文字表情实体识别、属性检测、新颜发现等。

### 生成适用于 Rime 输入法的词库

一般情况下如果您没有开发需求，您可以直接前往  [releases](https://github.com/aoguai/rime_kaomoji_dict/releases) 下载最新版本的词库文件，直接使用即可。

解压后你会得到两个适用于 Rime 输入法的词库文件
```html
kaomoji_kmj.dict.yaml
kaomoji_pinyin.dict.yaml
```
其中 `kaomoji_kmj.dict.yaml` 是颜文字词库，`kaomoji_pinyin.dict.yaml` 是颜文字拼音词库。

它们的区别在于：

`kaomoji_kmj.dict.yaml`：固定将**所有颜文字** **拼音部份（即文字对应的编码）** 设置为`kmj`

`kaomoji_pinyin.dict.yaml` ：则是正常使用 [Pypinyin](https://github.com/mozillazg/python-pinyin) 生成所有颜文字对应的中文的拼音[（可选双拼）](https://github.com/aoguai/rime_kaomoji_dict#双拼词库)作为文字对应的编码

二者互不冲突，您可以根据自己的喜好选择其一或全部将其放入 Rime 输入法的用户文件夹中并做对应的**调用**即可。

### 从项目仓库源码构建

同时您还可以自行从项目仓库源码构建词库
#### 全拼词库
```bash
git clone https://github.com/aoguai/rime_kaomoji_dict.git
cd rime_kaomoji_dict
pip install -r requirements.txt
python main.py
```
完成后，**默认**会在data 目录中生成
```html
all_output_result_kmj.txt
all_output_result_pinyin.txt
```
与 `kaomoji_kmj.dict.yaml` 和 `kaomoji_pinyin.dict.yaml`对应

同时，从本仓库源码构建时，您可以自行选择使用哪些颜文字素材，只需在 `main.py` 中修改 `input_filename_list` 变量即可。

同时你还可以自定义导出的词库的**格式**等，具体请自行查看 `main.py` 中的 `process_and_save_combined_kaomoji` 函数部分代码。
#### 双拼词库

切换至 [shuangpin](https://github.com/aoguai/rime_kaomoji_dict/tree/shuangpin) 分支
```bash
pip install Pinyin2Hanzi
python pydict2spdict.py
```
具体使用方法请参考 [shuangpin](https://github.com/aoguai/rime_kaomoji_dict/tree/shuangpin) 分支
## 鸣谢

### 数据原始来源

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
此存储库遵循 [MIT 开源协议](https://github.com/aoguai/rime_kaomoji_dict/blob/master/LICENSE)，请务必理解。

我们严禁所有通过本程序违反任何国家法律的行为，请在法律范围内使用本程序。

默认情况下，使用此项目将被视为您同意我们的规则。请务必遵守道德和法律标准。

如果您不遵守，您将对后果负责，作者将不承担任何责任！