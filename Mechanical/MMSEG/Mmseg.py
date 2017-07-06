# -*- coding:utf-8 -*-
import sys, traceback
sys.path.append('../../Dictionary')
sys.path.append('../')
from DictionaryFactory import DACTORY
from ReverseMaximumMatching import reverseMaximumMatching

def siple_mmseg(text):
  return reverseMaximumMatching(text)


if __name__ == '__main__':
  # print DACTORY.getNaiveDictionary().query('中国人')
  print DACTORY.getNaiveDictionary().query('色')
  # print len('武汉市'.decode('utf-8'))
  terms = siple_mmseg('武汉市长江大桥')
  print '|'.join(terms)
