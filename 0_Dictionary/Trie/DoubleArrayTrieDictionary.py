# -*- coding:utf-8 -*-
import sys, time, traceback
import os, pickle
from  TrieDictionary import TrieNode as TrieNode
__pwd__ = os.path.dirname(os.path.realpath(__file__))
class unit_t:
  def __init__(self, base, check):
    self.base = base
    self.check = check
  def __str__(self):
    return str((self.base,self.check))

class DoubleArrayTrieDictionary:

  def __init__(self):
    self.array = []
    self.used = []
    self.word_cnt = 0
    self.progress = 0
    self.base_used_cnt = 0
    self.check_used_cnt = 0
    self.load_cost = 0
    self.build_cost = 0
    self.max_word_length = 0
  def __resize__(self, size):
    if len(self.array)<size:
      new_array = [unit_t(0,0) for x in xrange(0,size)]
      new_used = [0 for x in xrange(0,size)]
      i=0
      while i<len(self.array):
        new_array[i] = self.array[i]
        new_used[i] = self.used[i]
        i+=1
      self.array = new_array
      self.used = new_used
      # print [str(x) for x in self.array]
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
          if new_node.depth > self.max_word_length:
            self.max_word_length = new_node.depth
          new_node.left = i
          if len(parent.siblings)>0:
            parent.siblings[-1].right = i
          parent.siblings.append(new_node)
        pre = cur 
      i += 1
    if len(parent.siblings)>0:
      parent.siblings[-1].right = i
    return len(parent.siblings)
  def __locate_base__(self, node):
    cur_s = 1
    while True:
      if not cur_s+node.siblings[-1].code<len(self.array):
        self.__resize__(cur_s+node.siblings[-1].code+1+1024)
      if self.used[cur_s]:
        cur_s += 1
        continue
      t = cur_s + node.siblings[0].code
      i = 0
      while i<len(node.siblings) and self.array[t].check==0:
        i += 1
      else:
        if i==len(node.siblings):
          self.used[cur_s] = True
          return cur_s
        else:
          cur_s += 1
  def __insert_array__(self, parent, dic):
    begin = self.__locate_base__(parent)
    # print len(self.array)
    i = 0
    while i<len(parent.siblings):
      # print base+root.siblings[i].code
      self.array[begin+parent.siblings[i].code].check = begin
      self.check_used_cnt += 1
      i+=1
    # self.array[begin].base = base
    # print self.array[begin]
    for node in parent.siblings:
      # 如果node是一个叶子节点，那么它的code一定是0，所以当前t = base[s]+0 = base[s]
      # 因为这是一个终止状态，所以将base[s+0]设为负值
      if self.__generate_siblings__(node, dic)==0:
        self.array[begin].base = -parent.left-1
        # print begin, self.array[begin]
        self.progress += 1
        self.base_used_cnt += 1
        print 'Progress: %d/%d' % (self.progress,self.word_cnt)
      else:
        self.array[begin+node.code].base = self.__insert_array__(node, dic)
        self.base_used_cnt += 1
    return begin

  def build(self, dic):
    words = [x.strip().split('\t')[0].decode('utf-8') for x in open(dic)]
    words.sort()
    self.word_cnt = len(words)
    # self.__resize__(8192)
    self.__resize__(2)
    self.array[0].base = 1
    # self.array[1].check = 0
    # self.__resize__(10)
    root = TrieNode()
    root.code = 0
    root.depth = 0
    root.left = 0
    root.right = len(words)
    siblings = self.__generate_siblings__(root, words)
    # print root
    self.__insert_array__(root, words)
    # print [str(x) for x in self.array]
    self.used = None
  def statistics(self):
    return 'size in bytes: '+str(sys.getsizeof(self.array))+'\nbuild cost: '+str(self.build_cost)+'\nload cost: '+str(self.load_cost)+'\ncheck used rate: '+str(self.check_used_cnt)+'/'+str(len(self.array))+'\nbase used rate: '+str(self.base_used_cnt)+'/'+str(len(self.array))+'\nmax word length: '+str(self.max_word_length)
  
  def save(self, name):
    to_save_file = name+'.bin'
    f = None
    try:
      f = file(to_save_file, 'wb')
      pickle.dump((self.max_word_length,self.array), f)
    except:
      traceback.print_exc()
    finally:
      if f:
        f.close()
  def load(self, name):
    from_load_file = name + '.bin'
    f = None
    try:
      f = file(from_load_file, 'rb')
      b = time.clock()
      self.max_word_length, self.array = pickle.load(f)
      e = time.clock()
      self.load_cost = e-b
    except:
      traceback.print_exc()
      return False
    finally:
      if f:
        f.close()
    return True

  def initialize(self, dict_name=__pwd__+'/../dict/SogouLabDic.utf8.dic'):
    if not self.load(dict_name):
      b = time.clock()
      self.build(dict_name)
      e = time.clock()
      self.build_cost = e-b
      self.save(dict_name)
    return self.statistics()

  def query(self, term):
    state = 0
    i = 0
    next_state = self.array[state].base+ord(term[i])+1
    # print state, self.array[state], ord(term[i]), next_state, self.array[next_state]
    while i<=len(term):
      if not self.array[next_state].check == self.array[state].base:
        break
      state = next_state
      i += 1
      if i>len(term):
        break
      c = 0 if i==len(term) else ord(term[i])+1
      next_state = self.array[state].base+c
      # print state, self.array[state], c, next_state, self.array[next_state]
    return (i-1)==len(term) and self.array[state].base < 0

if __name__ == '__main__':
  da = DoubleArrayTrieDictionary()
  # da.initialize(__pwd__+'/../dict/test.dic')
  # da.build(__pwd__+'/../dict/test.dic')
  # print da.initialize(__pwd__+'/../dict/test.dic')
  # da.build('test_10000.dic')
  # da.initialize(__pwd__+'/../dict/test_10000.dic')
  # da.build('SogouLabDic.utf8.dic')
  # da.initialize('SogouLabDic.utf8.dic')
  # print da.statistics()
  print da.initialize()
  print da.query('一举'.decode('utf-8'))
  print da.query('一举一动'.decode('utf-8'))
  print da.query('万能胶水'.decode('utf-8'))
  print da.query('万能胶'.decode('utf-8'))
  print da.query('化为己有'.decode('utf-8'))
