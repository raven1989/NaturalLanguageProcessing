# -*- coding:utf-8 -*-
# 算法复杂度是o(N)
import sys, traceback
sys.path.append('../0_Dictionary')
from DictionaryFactory import DACTORY

def reverseMaximumMatching(text):
  uniText = text.decode('utf-8')
  terms = []
  size = len(uniText)
  dic = DACTORY.getNaiveDictionary()
  end = size
  maxSize = dic.query('maxTermSize')
  while end>0:
    curSize = end
    start = end - min(curSize, maxSize)
    # print uniText[start:end]
    while end-start>1 and not dic.query(uniText[start:end].encode('utf-8')):
      start += 1
    terms.append(uniText[start:end])
    end = start
  terms.reverse()
  return map(lambda x: x.encode('utf-8'), terms)


if __name__ == '__main__':
  # print DACTORY.getNaiveDictionary().query('中国人')
  print DACTORY.getNaiveDictionary().query('人')
  # print len('武汉市'.decode('utf-8'))
  terms = reverseMaximumMatching('武汉市长江大桥')
  print '|'.join(terms)
