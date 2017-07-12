# -*- coding:utf-8 -*-
import sys, traceback
import os
import TrieDictionary.TrieNode as TrieNode
__pwd__ = os.path.dirname(os.path.realpath(__file__))

class DoubleArrayTrieDictionary:
  class unit_t:
    def __init__(self, base, check):
      self.base = base
      self.check = check

  def __init__(self):
    self.array = []
  def __resize__(self, size, value=unit_t(0,0)):
    if len(self.array)<size:
      self.array.extend([value]*(size-len(self.array)))
  def __locate_base__(self, s, node):
    cur_s = s
    while True:
      t = cur_s + node.siblings[0].code
      if not cur_s+len(node.siblings[-1].code)<len(self.array):
        self.__resize__(cur_s+len(node.siblings[-1].code+1+128))
      i = 0
      while i<len(node.siblings) and array[t].check==0:
        i += 1
      else:
        if i==len(node.siblings):
          return t
        else:
          i = 0
          cur_s += 1
  def __generate_siblings__(self, node, words):
    i = node.left
    cnt = 0
    while i<node.right:
      word = word[i]
      if len(word)<node.depth+1:
        if len(word)==node.depth+1:
          empty_node = TrieNode()
          empty_node.code = 0
          empty_node.depth = node.depth+1
          empty_node.left = node.left
          empty_node.right = node.left+1
          node.siblings.append(empty_node)
        else:
          if word[pre.code!=word[i].code:
            new_node = TrieNode()
            new_node.code = ord(word[node.depth+1])+1
            new_node.depth = node.depth+1
            new_node.left = node.siblings[-1].right if len(node.siblings)>0 else node.left
            new_node.right = node.siblings[-1].
      pre = i
      i += 1

  def build(self):
    words = [x.strip().decode('utf-8') for x in open(__pwd__+'/../dict/'+dic)]
    words.sort()
    root = TrieNode()
    root.code = 0
    root.depth = 0
    root.left = 0
    root.right = len(words)


if __name__ == '__main__':
  print ord('一'.decode('utf-8'))
  print ord('万'.decode('utf-8'))
