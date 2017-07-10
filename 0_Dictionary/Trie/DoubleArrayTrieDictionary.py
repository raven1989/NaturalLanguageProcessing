# -*- coding:utf-8 -*-
import sys, traceback
import os
__pwd__ = os.path.dirname(os.path.realpath(__file__))

class CharDictionary:
  def __init__(self):
    self.dic_ = {}
    self.load_char_dictionary()
  def load_char_dictionary(self):
    self.dic_['total'] = 0
    for line in open(__pwd__+'/dict/chars.dic'):
      col = line.split(' ')
      if len(col)<2:
        continue
      self.dic_[col[0]] = int(col[1])
      self.dic_['total'] += 1
  def query(self, term):
    if not self.dic_.has_key(term):
      return False
    return self.dic_[term]

if __name__ == '__main__':
  print ord('一'.decode('utf-8'))
