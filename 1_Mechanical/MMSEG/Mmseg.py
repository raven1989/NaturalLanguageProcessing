# -*- coding:utf-8 -*-
import sys, traceback
import math
sys.path.append('../../0_Dictionary')
sys.path.append('../')
from DictionaryFactory import DACTORY
from ReverseMaximumMatching import reverseMaximumMatching

def siple_mmseg(text):
  return reverseMaximumMatching(text)

#--------------------------------------------------------------------------------

def complex_mmseg(text):
  unicode_text = text.decode('utf-8')
  text_length = len(unicode_text)
  start = 0
  res = []
  # rule 2: 平均词长
  mean_for_words = lambda x : x[-1]/float(len(x))
  # print 'mean_for_words test :', mean_for_words(0,(1,2))
  # rule 3: 词长方差
  variance_for_words = lambda x,mean : sum([(i-mean)**2 for i in x])/float(len(x))
  while start<text_length:
    triplets = get_longest_triplets_for_1st_char(unicode_text[start:])
    rule = 1
    max_mean = 0
    while len(triplets)>1 and rule<4:
      # print rule, triplets
      if rule==1:
        max_mean = max([mean_for_words(x) for x in triplets])
        # print triplets, max_mean
        triplets = filter(lambda x:mean_for_words(x)>=max_mean, triplets)
      elif rule==2:
        min_variance = min([variance_for_words(x,max_mean) for x in triplets])
        triplets = filter(lambda x:variance_for_words(x,max_mean)<=min_variance, triplets)
      else:
        # 最后一个rule，就算有多个满足条件也不能再处理了，就直接交给max取其中一个
        triplets = [max(triplets, key = lambda x:ln_frequency_for_sigle_chars(unicode_text[start:], x))]
      rule += 1
    # print rule, triplets
    res.append(unicode_text[start:start+triplets[0][0]])
    start += triplets[0][0]
    # print 'start:',start
    # print '|'.join(res)
  return [x.encode('utf-8') for x in res]


# rule 1 : 最长三词trunk
# tree node : (start+length, father, level)
# input : str coded as unicode
# input : start index, default 0
# return : (length1, [length2, length3])
# whith start from inputs, 3-word-trunk is completely denoted
def get_longest_triplets_for_1st_char(unicode_text, start=0):
  char = unicode_text[start]
  root = (start+0, -1, 0)
  father = 0
  def forward_matching(text):
    length = 1
    max_length = min(len(text), DACTORY.getNaiveDictionary().query('maxTermSize'))
    while length<=max_length:
      # condition length==1 是为了将单字也输出为结果，因为词典里面没有包含单字
      if length==1 or DACTORY.getNaiveDictionary().query(text[:length].encode('utf-8')):
        yield length
      length += 1
  tree = [root]
  i = 0
  # 广度优先构造tree
  # condition tree[i][1]<len(unicode_text[start:]) 是为了保证在不够三个词的情况下的正确性
  while i<len(tree) and tree[i][1]<len(unicode_text[start:]) and tree[i][2]<3:
    children = [(tree[i][0]+x, i, tree[i][2]+1) 
        for x in forward_matching(
          # 父节点的长度意味着切割，也就是下一次匹配的开始索引
          unicode_text[tree[i][0]:]
          )
        ]
    tree += children
    i += 1
  # print tree
  # 按照rule1的规则，寻找字数最多的triplets
  max_node = max(tree, key = lambda x:x[0])
  max_nodes = filter(lambda x:x[0]>=max_node[0], tree)
  # 寻根路径
  def travel_to_root(node, tree):
    start = node
    while start[1]>=0:
      yield start[0]
      start = tree[start[1]]
  res = map(lambda x:tuple([y for y in travel_to_root(x, tree)][::-1]), 
      max_nodes)
  return res

# rule 4: 单字词频对数和
def ln_frequency_for_sigle_chars(unicode_text, triplets):
  def sigle_char(unicode_text, triplets):
    i = 0
    for l in triplets:
      if l-i==1:
        yield unicode_text[i:l]
      i = l
  sigle_chars = [x for x in sigle_char(unicode_text, triplets)]
  # print 'sigle chars:', '|'.join(sigle_chars)
  ln_freq = []
  for char in sigle_chars:
    freq = DACTORY.get_char_dictionary().query(char.encode('utf-8'))
    if freq:
      # print freq
      ln_freq.append(math.log(int(freq)))
  # print ln_freq
  return reduce(lambda x,y:x+y,ln_freq)
  


if __name__ == '__main__':
  print DACTORY.getNaiveDictionary().query('长江大桥')
  print DACTORY.getNaiveDictionary().query('科学')
  # 居然还有"和服务"这种词，为了测试规则四只能手动删了
  print DACTORY.getNaiveDictionary().query('和服务')
  DACTORY.getNaiveDictionary().dic_.pop('和服务')
  print DACTORY.getNaiveDictionary().query('和服务')
  print DACTORY.getNaiveDictionary().query('施和')
  # print DACTORY.getNaiveDictionary().query('色')
  # print len('武汉市'.decode('utf-8'))
  # print '|'.join(siple_mmseg('武汉市长江大桥'))
  # print get_longest_triplets_for_1st_char('武汉市长江大桥'.decode('utf-8'))
  # print get_longest_triplets_for_1st_char('武汉市'.decode('utf-8'))
  # print get_longest_triplets_for_1st_char('研究生命科学'.decode('utf-8'))
  # print get_longest_triplets_for_1st_char('科学'.decode('utf-8'))
  # terms = siple_mmseg('研究生命科学')
  print '|'.join(complex_mmseg('研究生命科学'))
  print '|'.join(complex_mmseg('武汉市长江大桥'))
  print '|'.join(complex_mmseg('声明科学'))
  print '|'.join(complex_mmseg('设施和服务'))

