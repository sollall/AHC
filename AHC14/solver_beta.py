# coding: utf-8
# Your code here!
import time

import numpy as np
from scipy.sparse.csgraph import shortest_path, floyd_warshall, dijkstra, bellman_ford, johnson
from scipy.sparse import csr_matrix, lil_matrix

start_time=time.time()

N,M=map(int,input().split())

fields=[[0 for i in range(N)] for j in range(N)]

for _ in range(M):
    x,y=map(int,input().split())
    fields[x][y]=1
    
class Solver:
    def __init__(self,fields):
        self.fields=fields
        self.N=len(fields)
    
    def search(self,h,w):
        #とりあえず上下左右の点を探して、あったら対角か一辺としてみていけばいいのでは
        options=[]
        for i in range(self.N):
            if fields[i][w]==1 and i!=h:
                options.append([i,w])
            if fields[h][i]==1 and i!=w:
                options.append([h,i])
        while options:
            hh,ww=options.pop(-1)
            #対角とした場合
            diag=abs(h-hh)+abs(w-ww)#どっちかはゼロにはなるはずなんだけど
            if diag%2==0:#こうじゃないとほかの点が整数で表せない
                hc,wc=(h+hh)//2,(w+ww)//2
                if w==wc:
                    if fields[hc][wc+diag//2]==1 and fields[hc][wc-diag//2]==0:
                        fields[hc][wc-diag//2]=1
                        ans.append([hc,wc-diag//2,h,w,hc,wc+diag//2,hh,ww])
                    elif fields[hc][wc+diag//2]==0 and fields[hc][wc-diag//2]==1:
                        fields[hc][wc+diag//2]=1
                        ans.append([hc,wc+diag//2,h,w,hc,wc-diag//2,hh,ww])
                else:
                    if fields[hc+diag//2][wc]==1 and fields[hc-diag//2][wc]==0:
                        fields[hc-diag//2][wc]=1
                        ans.append([h,w,hh,ww,hc+diag//2,wc,hc-diag//2,wc])
                    elif fields[hc+diag//2][wc]==0 and fields[hc-diag//2][wc]==1:
                        fields[hc+diag//2][wc]=1
                        ans.append([h,w,hh,ww,hc+diag//2,wc,hc-diag//2,wc])
                    
solver=Solver(fields)
#solver.search(13,24)
h=0
ans=[]
while time.time()-start_time<=1.7:
    h=(h+1)%N
    for w in range(N):
        if fields[h][w]==1:
            solver.search(h,w)
print(len(ans))
for item in ans:
    print(*item)
