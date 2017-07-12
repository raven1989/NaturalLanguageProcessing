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
    self.default = self.unit_t(0,0)
  def __resize__(self, size, default):
    if len(self.array)<size:
      self.array.extend([default]*(size-len(self.array)))
      print [str(x) for x in self.array]
  def __locate_base__(self, s, node):
    cur_s = s
    while True:
      t = cur_s + node.siblings[0].code
      if not cur_s+node.siblings[-1].code<len(self.array):
        self.__resize__(cur_s+node.siblings[-1].code+1+128, self.default)
      i = 0
      while i<len(node.siblings) and self.array[t].check==0:
        i += 1
      else:
        if i==len(node.siblings):
          return cur_s
        else:
          i = 0
          cur_s += 1
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
  def __insert_array__(self, s, root):
    begin = s
    base = self.__locate_base__(s, root)
    print base
    print len(self.array)
    i = 0
    while i<len(root.siblings):
      print base+root.siblings[i].code
      # print [str(x) for x in self.array]
      self.array[base+root.siblings[i].code].check = begin
      i+=1
    self.array[begin].base = base
    print [str(x) for x in self.array]

  def build(self, dic):
    words = [x.strip().decode('utf-8') for x in open(__pwd__+'/../dict/'+dic)]
    words.sort()
    self.__resize__(8192, self.default)
    self.array[0].base = 1
    self.array[1].check = 0
    root = TrieNode()
    root.code = 0
    root.depth = 0
    root.left = 0
    root.right = len(words)
    siblings = self.__generate_siblings__(root, words)
    print root
    self.__insert_array__(2, root)


if __name__ == '__main__':
  da = DoubleArrayTrieDictionary()
  da.build('test.dic')
