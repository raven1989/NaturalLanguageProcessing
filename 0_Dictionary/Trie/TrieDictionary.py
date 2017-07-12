# -*- coding:utf-8 -*-
import sys, traceback
import os
__pwd__ = os.path.dirname(os.path.realpath(__file__))

class TrieNode:
  def __init__(self):
    self.code = 0
    self.depth = 0
    self.left = 0
    self.right = 0
    self.siblings = []
  def is_leaf(self):
    return len(self.siblings)==0
  # 利用递归展示一棵树
  def __str__(self):
    indent = ''.join(map(lambda x:'  ', xrange(0,self.depth)))
    return indent + '{'+ ','.join(
        [
          'code:'+str(0 if not self.code else unichr(self.code-1).encode('utf-8')), 
          'depth:'+str(self.depth), 
          'left:'+str(self.left), 
          'right:'+str(self.right), 
          'siblings:[\n'+ indent + ('\n'+indent).join(map(lambda x: str(x), self.siblings)) + ']',
        ]) + '}'

# dfs 构建trie tree
def build_trie_dictionary(dic):
  words = [x.strip().decode('utf-8') for x in open(__pwd__+'/../dict/'+dic)]
  # 使用字典序，有很多好处
  words.sort()
  for it in words:
    print it
  # code=0作为特殊标记使用，其他的字符编码全部加1，让出0
  root = TrieNode()
  stack = []
  for word in words:
    stack.append(root)
    new_word = False
    # 入栈开始，同时修改left
    i = 0
    while i<len(word):
      char = word[i]
      if stack[-1].is_leaf() or not stack[-1].siblings[-1].code == ord(char)+1:
        new_node = TrieNode()
        new_node.code = ord(char)+1
        new_node.left = max(stack[-1].left, stack[-1].right)
        new_node.depth = stack[-1].depth+1
        stack[-1].siblings.append(new_node)
        new_word = True
      stack.append(stack[-1].siblings[-1])
      i += 1
    else:
      # 添加一个空节点，表示这个路径成词
      if new_word:
        empty_node = TrieNode()
        empty_node.code = 0
        empty_node.left = max(stack[-1].left, stack[-1].right)
        empty_node.depth = stack[-1].depth + 1
        stack[-1].siblings.append(empty_node)
        stack.append(empty_node)
    # 弹栈开始，同时修改right
    while len(stack)>0:
      cur = stack.pop()
      cur.right += ( cur.left + (1 if new_word else 0) )
  return root

if __name__ == '__main__':
  root = build_trie_dictionary('test.dic')
  print root

