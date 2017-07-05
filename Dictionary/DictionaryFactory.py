# -*- coding:utf-8 -*-
import sys, traceback
import NaiveDictionary

class DictionaryFactory:
  def __init__(self):
    self.naive_ = None
  def getNaiveDictionary(self):
    if not self.naive_:
      self.naive_ = NaiveDictionary.NaiveDictionary()
    return self.naive_

DACTORY = DictionaryFactory()

if __name__ == '__main__':
  print DACTORY.getNaiveDictionary().query('中国人')

