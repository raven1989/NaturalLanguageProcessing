# -*- coding:utf-8 -*-
import sys, traceback
import os
__pwd__ = os.path.dirname(os.path.realpath(__file__))

class NaiveDictionary:
  def __init__(self):
    self.dic_ = {}
    self.loadSougouDictionary()
  def loadSougouDictionary(self):
    self.dic_['total'] = 0
    self.dic_['maxTermSize'] = 0
    for line in open(__pwd__+'/SogouLabDic.utf8.dic'):
      col = line.split('\t')
      if len(col)<3:
        continue
      self.dic_[col[0]] = int(col[1])
      if len(col[0])>self.dic_['maxTermSize']:
        self.dic_['maxTermSize'] = len(col[0])
      self.dic_['total'] += 1
  def query(self, term):
    if not self.dic_.has_key(term):
      return False
    return self.dic_[term]

if __name__ == '__main__':
  dic = NaiveDictionary()
  print dic.query('total')
  print dic.query('maxTermSize')
  print __pwd__
  print len('中国人')
