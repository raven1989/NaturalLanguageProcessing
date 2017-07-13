# -*- coding:utf-8 -*-
import sys, traceback
import os
from  TrieDictionary import TrieNode as TrieNode
__pwd__ = os.path.dirname(os.path.realpath(__file__))

class DoubleArrayTrieDictionary:
  class unit_t:
    def __init__(self, base, check):
      self.base = base
      self.check = check
    def __str__(self):
      return str((self.base,self.check))

  def __init__(self):
    self.array = []
    self.used = []
    self.word_cnt = 0
    self.progress = 0
  def __resize__(self, size):
    if len(self.array)<size:
      new_array = [self.unit_t(0,0) for x in xrange(0,size)]
      new_used = [0 for x in xrange(0,size)]
      i=0
      while i<len(self.array):
        new_array[i] = self.array[i]
        new_used[i] = self.used[i]
        i+=1
      self.array = new_array
      self.used = new_used
      # print [str(x) for x in self.array]
  def __generate_siblings__(self, parent, words):
    i = parent.left
    pre = 0
    while i<parent.right:
      word = words[i]
      if not len(word)<parent.depth:
        cur = 0 if len(word)==parent.depth else ord(word[parent.depth])+1
        if  len(parent.siblings)==0 or pre!=cur:
          new_node = TrieNode()
          new_node.code = cur
          new_node.depth = parent.depth+1
          new_node.left = i
          if len(parent.siblings)>0:
            parent.siblings[-1].right = i
          parent.siblings.append(new_node)
        pre = cur 
      i += 1
    if len(parent.siblings)>0:
      parent.siblings[-1].right = i
    return len(parent.siblings)
  def __locate_base__(self, node):
    cur_s = max(node.code, 1)
    while True:
      if not cur_s+node.siblings[-1].code<len(self.array):
        self.__resize__(cur_s+node.siblings[-1].code+1+128)
      if self.used[cur_s]:
        cur_s += 1
        continue
      t = cur_s + node.siblings[0].code
      i = 0
      while i<len(node.siblings) and self.array[t].check==0:
        i += 1
      else:
        if i==len(node.siblings):
          self.used[cur_s] = True
          return cur_s
        else:
          cur_s += 1
  def __insert_array__(self, parent, dic):
    begin = self.__locate_base__(parent)
    # print len(self.array)
    i = 0
    while i<len(parent.siblings):
      # print base+root.siblings[i].code
      self.array[begin+parent.siblings[i].code].check = begin
      i+=1
    # self.array[begin].base = base
    # print self.array[begin]
    for node in parent.siblings:
      # 如果node是一个叶子节点，那么它的code一定是0，所以当前t = base[s]+0 = base[s]
      # 因为这是一个终止状态，所以将base[s+0]设为负值
      if not self.__generate_siblings__(node, dic):
        self.array[begin+0].base = -parent.left-1
        self.progress += 1
        print 'Progress: %d/%d' % (self.progress,self.word_cnt)
      else:
        self.array[begin+node.code].base = self.__insert_array__(node, dic)
    return begin

  def build(self, dic):
    words = [x.strip().decode('utf-8') for x in open(__pwd__+'/../dict/'+dic)]
    words.sort()
    self.word_cnt = len(words)
    # self.__resize__(8192)
    self.__resize__(2)
    self.array[0].base = 1
    # self.array[1].check = 0
    self.__resize__(10)
    root = TrieNode()
    root.code = 0
    root.depth = 0
    root.left = 0
    root.right = len(words)
    siblings = self.__generate_siblings__(root, words)
    # print root
    self.__insert_array__(root, words)
    print [str(x) for x in self.array]

if __name__ == '__main__':
  da = DoubleArrayTrieDictionary()
  da.build('test1.dic')
