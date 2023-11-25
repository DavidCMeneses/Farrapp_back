import numpy as np
from queue import Queue 
from collections import deque
from .models import EstablishmentModel

trie = [np.zeros(40, dtype=int)]
est = [[]]

def idx(c):
  if c == '.':
    return 37
  if c==' ':  
    return 36
  if c>='A' and c<='Z':
    return ord(c)-ord('A')
  if c>='0' and c<='9':
    return 26 + ord(c) - ord('0')
  return ord(c)-ord('a')

def add_trie (s, id):
  node = 0
  est[0].append(id)
  for i in range(len(s)):
    if trie[node][idx(s[i])] == 0:
      trie[node][idx(s[i])] = len(trie)
      trie.append(np.zeros(40, dtype=int))
      est.append([])
    node = trie[node][idx(s[i])]
    est[node].append(id)


def add_establishment (name, id):
  add_trie(name, id)
  for i in range(len(name)):
    if i > 0 and name[i-1] == ' ':
      add_trie(name[i:], id)

def search_est (name):
  print("woli")
  for e in EstablishmentModel.objects.all():
    add_establishment(e.name, e.pk)

  q=deque()
  q.append([0,0,0])
  visi=set()
  visi.add((0,0))
  LS=[[],[],[]]
  n = len(name)

  while len(q) > 0:
    u = q.popleft()
    if u[1] == n:
      for e in est[u[0]]:
        LS[u[2]].append(e)
    else:
      nu = [u[0],u[1]+1,u[2]+1]
      if (nu[0],nu[1]) not in visi and nu[2]<3:
        visi.add((nu[0],nu[1]))
        q.append(nu)
      
      if trie[u[0]][idx(name[u[1]])] > 0:
        nu = [trie[u[0]][idx(name[u[1]])], u[1]+1, u[2]]
        if (nu[0],nu[1]) not in visi and nu[2]<3:
            visi.add((nu[0],nu[1]))
            q.appendleft(nu)
      
      for i in range(40):
        if trie[u[0]][i] > 0:
          nu = [trie[u[0]][i],u[1],u[2]+1]
          if (nu[0],nu[1]) not in visi and nu[2]<3:
            visi.add((nu[0],nu[1]))
            q.append(nu)
          nu = [trie[u[0]][i],u[1]+1,u[2]+1]
          if (nu[0],nu[1]) not in visi and nu[2]<3:
            visi.add((nu[0],nu[1]))
            q.append(nu)
  
  lsall = []
  unq=set()
  for i in range(3):
    for e in LS[i]:
      if e not in unq:
        lsall.append(e)
        unq.add(e)
  
  return lsall
  
