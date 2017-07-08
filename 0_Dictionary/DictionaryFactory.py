# -*- coding:utf-8 -*-
import sys, traceback
import NaiveDictionary
import CharDictionary

class DictionaryFactory:
  def __init__(self):
    self.naive_ = None
    self.char_ = None
  def getNaiveDictionary(self):
    if not self.naive_:
      self.naive_ = NaiveDictionary.NaiveDictionary()
    return self.naive_
  def get_char_dictionary(self):
    if not self.char_:
      self.char_ = CharDictionary.CharDictionary()
    return self.char_

DACTORY = DictionaryFactory()

if __name__ == '__main__':
  print DACTORY.getNaiveDictionary().query('中国人')
  print DACTORY.get_char_dictionary().query('中')

