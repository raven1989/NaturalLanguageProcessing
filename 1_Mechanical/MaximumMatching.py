# -*- coding:utf-8 -*-
# 算法复杂度是o(N)
import sys, traceback
sys.path.append('../0_Dictionary')
from DictionaryFactory import DACTORY

def maximumMatching(text):
  uniText = text.decode('utf-8')
  terms = []
  size = len(uniText)
  dic = DACTORY.getNaiveDictionary()
  start = 0
  maxSize = dic.query('maxTermSize')
  while start<size:
    curSize = size-start
    end = start + min(curSize, maxSize)
    # print uniText[start:end]
    while end-start>1 and not dic.query(uniText[start:end].encode('utf-8')):
      end -= 1
    terms.append(uniText[start:end])
    start = end
  return map(lambda x: x.encode('utf-8'), terms)


if __name__ == '__main__':
  print DACTORY.getNaiveDictionary().query('中国人')
  print DACTORY.getNaiveDictionary().query('武汉市')
  print len('武汉市'.decode('utf-8'))
  terms = maximumMatching('武汉市长江大桥')
  print '|'.join(terms)
