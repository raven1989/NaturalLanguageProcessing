# -*- coding:utf-8 -*-
import sys, traceback
import Naive.NaiveDictionary as NaiveDictionary
import Char.CharDictionary as CharDictionary
import Trie.DoubleArrayTrieDictionary as DoubleArrayTrieDictionary
from Trie.DoubleArrayTrieDictionary import unit_t as unit_t

class DictionaryFactory:
  def __init__(self):
    self.naive_ = None
    self.char_ = None
    self.da_trie_ = None
  def getNaiveDictionary(self):
    if not self.naive_:
      self.naive_ = NaiveDictionary.NaiveDictionary()
    return self.naive_
  def get_char_dictionary(self):
    if not self.char_:
      self.char_ = CharDictionary.CharDictionary()
    return self.char_
  def get_da_trie_dictionary(self):
    if not self.da_trie_:
      self.da_trie_ = DoubleArrayTrieDictionary.DoubleArrayTrieDictionary()
      print self.da_trie_.initialize()
    return self.da_trie_

DACTORY = DictionaryFactory()

if __name__ == '__main__':
  print DACTORY.getNaiveDictionary().query('中国人')
  print DACTORY.get_char_dictionary().query('中')
  print DACTORY.get_da_trie_dictionary().query('彼方'.decode('utf-8'))
  print DACTORY.get_da_trie_dictionary().query('武汉'.decode('utf-8'))
  # print DACTORY.get_da_trie_dictionary().statistics()

