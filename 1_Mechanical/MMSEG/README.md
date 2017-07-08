# MMSEG

### 1. 概念

#### 匹配算法：

1. 简单匹配：其实就是最大匹配(MM,RMM都可以)

  即简单的正向匹配，根据开头的字，列出所有可能的结果。比如“一个劲儿的说话”，可以得到

  一个
  
  一个劲

  一个劲儿

  一个劲儿的

  这四个匹配结果（假设这四个词都包含在词典里）。

2. 复杂匹配：

  匹配出所有的“三个词的词组”（原文中使用了chunk，这里感觉用“词组”比较合适），即从某一既定的字为起始位置，得到所有可能的“以三个词为一组”的所有组合。比如“研究生命起源”，可以得到

  研_究_生

  研_究_生命

  研究生_命_起源

  研究_生命_起源

  这些“词组”（根据词典，可能远不止这些，仅此举例）

  “消除歧义的规则”有四个，使用中依次用这四个规则进行过滤，直到只有一种结果或者第四个规则使用完毕

#### 歧义消解规则：

rule 1: 找出字数最多的三词组

rule 2: 找出平均词长最大的三词组

rule 3: 找出词组方差最小的三词组

rule 4: 找出单字频率对数和最大的三词组

### 2. 模型

example: 武汉市长江大桥

mmseg要求获得三词组的全切分，用当前字查词典获得所有以该字为前缀的词，依次对每个词进行三轮：

大致产生过程如下图1

![树型模型](https://github.com/raven1989/NaturalLanguageProcessing/tree/master/1_Mechanical/MMSEG/photo/model_3word_trunk_tree.png)

再将图1进一步抽象：

1. 用当前词到开头位置的长度（包括当前词）代替标示一个节点，那么从根到叶子产生的序列就可以表示每一个词组的分割：

   example: (2,4,5) : 武汉，市长，江

2. 用父指针组织树，有利于寻找rule1要求的拥有最长字数的三词组，就是节点里数字最大的那些节点，再寻回到根既是

观察图中的树，会发现很多节点是相同的，那么把相同的节点合并，就会得到下图：

![图模型](https://github.com/raven1989/NaturalLanguageProcessing/blob/master/1_Mechanical/MMSEG/photo/model_3word_trunk_graph.png)

边上的数字表示能到达起点0的最小跳数，最大的跳数一定是3跳，

对于字数最长的三词组，起点是0，终点一定是数字最大的节点，比如图3中的5，

那么问题又可以抽象为以0为起点，5为终点，寻找所有的最短路径（一定是3跳）,

example: (0,2,3,5), (0,2,4,5)

思路：从5出发遍历所有入边，找出跳数最小的边的终点，继续依照上述规则遍历直到0


因为图的模型和算法都比较复杂，所以这里实现采用树的模型；

树的模型数据有冗余，所谓以空间换时间


> 参考文章：

[MMSEG: A Word Identification System for Mandarin Chinese Text Based on Two Variants of the Maximum Matching Algorithm](http://technology.chtsai.org/mmseg/)

[mmseg分词算法及实现](http://blog.csdn.net/daniel_ustc/article/details/50488040)

[关于MMSEG分词算法](http://blog.csdn.net/watkinsong/article/details/37872683)
