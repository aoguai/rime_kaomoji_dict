#!/usr/bin/python
# Author：wkong、

def DynamicProgramming(word, wordList, pinyinListStr=''):
    wordLen = len(word)

    for i in range(0, wordLen+1):
        pList = pinyinListStr.split(',')
        if word[0:i] in wordList:
            if i == wordLen:
                pList.append(word[0:i])
                print('Success:')
                print(pList)
            else:
                pList.append(word[0:i])
                DynamicProgramming(word[i:], wordList, ','.join(pList))

if __name__ == '__main__':
    smList = 'b,p,m,f,d,t,n,l,g,k,h,j,q,x,zh,ch,sh,r,z,c,s,y,w'.split(',')
    ymList = 'a,o,e,i,u,v,ai,ei,ui,ao,ou,iu,ie,ve,er,an,en,in,un,vn,ang,eng,ing,ong'.split(',')
    # ztrdList = 'zhi,chi,shi,ri,zi,ci,si,yi,wu,yu,ye,yue,yuan,yin,yun,ying'.split(',')
    ztrdList = 'a,an,ang,ai,e,ei'.split(',')


    pyList = ['ai','an','ang','ao','ba','bai','ban','bang','bao','bei','ben','beng','bi','bian','biao','bie','bin','bing','bo','bu','ca','cai','can','cang','cao','ce','cen','ceng','cha','chai','chan','chang','chao','che','chen','cheng','chi','chong','chou','chu','chua','chuai','chuan','chuang','chui','chun','chuo','ci','cong','cou','cu','cuan','cui','cun','cuo','da','dai','dan','dang','dao','de','den','dei','deng','di','dia','dian','diao','die','ding','diu','dong','dou','du','duan','dui','dun','duo','ei','en','eng','er','fa','fan','fang','fei','fen','feng','fo','fou','fu','ga','gai','gan','gang','gao','ge','gei','gen','geng','gong','gou','gu','gua','guai','guan','guang','gui','gun','guo','ha','hai','han','hang','hao','he','hei','hen','heng','hong','hou','hu','hua','huai','huan','huang','hui','hun','huo','ji','jia','jian','jiang','jiao','jie','jin','jing','jiong','jiu','ju','juan','jue','jun','ka','kai','kan','kang','kao','ke','ken','keng','kong','kou','ku','kua','kuai','kuan','kuang','kui','kun','kuo','la','lai','lan','lang','lao','le','lei','leng','li','lia','lian','liang','liao','lie','lin','ling','liu','long','lou','lu','lü','luan','lue','lüe','lun','luo','ma','mai','man','mang','mao','me','mei','men','meng','mi','mian','miao','mie','min','ming','miu','mo','mou','mu','na','nai','nan','nang','nao','ne','nei','nen','neng','ni','nian','niang','niao','nie','nin','ning','niu','nong','nou','nu','nü','nuan','nüe','nuo','nun','ou','pa','pai','pan','pang','pao','pei','pen','peng','pi','pian','piao','pie','pin','ping','po','pou','pu','qi','qia','qian','qiang','qiao','qie','qin','qing','qiong','qiu','qu','quan','que','qun','ran','rang','rao','re','ren','reng','ri','rong','rou','ru','ruan','rui','run','ruo','sa','sai','san','sang','sao','se','sen','seng','sha','shai','shan','shang','shao','she','shei','shen','sheng','shi','shou','shu','shua','shuai','shuan','shuang','shui','shun','shuo','si','song','sou','su','suan','sui','sun','suo','ta','tai','tan','tang','tao','te','teng','ti','tian','tiao','tie','ting','tong','tou','tu','tuan','tui','tun','tuo','wa','wai','wan','wang','wei','wen','weng','wo','wu','xi','xia','xian','xiang','xiao','xie','xin','xing','xiong','xiu','xu','xuan','xue','xun','ya','yan','yang','yao','ye','yi','yin','ying','yo','yong','you','yu','yuan','yue','yun','za','zai','zan','zang','zao','ze','zei','zen','zeng','zha','zhai','zhan','zhang','zhao','zhe','zhei','zhen','zheng','zhi','zhong','zhou','zhu','zhua','zhuai','zhuan','zhuang','zhui','zhun','zhuo','zi','zong','zou','zu','zuan','zui','zun','zuo'
              ] # 字典

    # 根据声母、韵母、整体认读音节排列组合出所有拼音字典
    # 这里为了方便演示，只加入了演示拼音涉及到的声母、韵母、整体认读音节
    for s in smList:
        for y in ymList:
            tmp = s+y
            if tmp not in pyList:
                pyList.append(tmp)

    for z in ztrdList:
        if z not in pyList:
            pyList.append(z)



    DynamicProgramming('guanepenge', pyList)
    print('----------------------')
    DynamicProgramming('guanapenga', pyList)
