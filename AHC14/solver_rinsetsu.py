# coding: utf-8
# Your code here!
import time
import numpy as np

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
        
        self.edges=self.make_edges()
        

    def xy2hash(self,x,y):
        return y*self.N+x
        
    def make_edges(self):
        edge=[{} for i in range(self.N*self.N)]
        for h in range(self.N):
            for w in range(self.N):
                pos=self.xy2hash(w,h)
                if pos//self.N!=0:
                    edge[pos][pos-self.N]=0
                if pos//self.N!=self.N-1:
                    edge[pos][pos+self.N]=0
                if pos%self.N!=0:
                    edge[pos][pos-1]=0
                if pos%self.N!=self.N-1:
                    edge[pos][pos+1]=0
                #ななめ
                if pos//self.N!=0 and pos%self.N!=0:
                    edge[pos][pos-self.N-1]=0
                if pos//self.N!=0 and pos%self.N!=self.N-1:
                    edge[pos][pos-self.N+1]=0
                if pos//self.N!=self.N-1 and pos%self.N!=0:
                    edge[pos][pos+self.N-1]=0
                if pos//self.N!=self.N-1 and pos%self.N!=N-1:
                    edge[pos][pos+self.N+1]=0                
                
        return edge

    def search_box(self,h,w):

        
    
    def generate(self,h,w,lr,ud,r_sheld,l_sheld):
        #pathを歩いてつぶしていかないといけない
        for a,b in lr:
            for c,d in ud:
                #h,w,a,b,c,dから4つめの点がでる
                #h,wから歩いて行ってedgeが使われていないことを確認しないといけない
                nh,nw=h+(a-h),w+(d-w)
                
                if fields[nh][nw]==0 and fields[a][b]==1 and fields[c][d]==1:#仮想なのはnh,nwだけにしなきゃいけない
                    yield [nh,nw,a,b,h,w,c,d]
    
    def check_edges(self,square):
        roots=[]
        for s in range(len(square)//2-1):
            h,w,nh,nw=square[(2*s)%len(square)],square[(2*s+1)%len(square)],square[(2*s+2)%len(square)],square[(2*s+3)%len(square)]
            h_dire=1 if nh-h>=0 else -1
            w_dire=1 if nw-w>=0 else -1
            for i in range(min(h,nh),max(h,nh)+1)[::h_dire]:
                for j in range(min(w,nw),max(w,nw)+1)[::w_dire]:
                    roots.append([i,j])
                    if len(roots)>1 and roots[-2]==[i,j]:#折り返し地点で被る対策
                        roots.pop(-1)
                    
        for i in range(len(roots)-1):
            s=roots[i][0]*self.N+roots[i][1]
            t=roots[i+1][0]*self.N+roots[i+1][1]
            if self.edges[min(s,t)][max(s,t)]==1:
                return False
        #ここ以下からpassした場合 変更を加える
        for i in range(len(roots)-1):
            s=roots[i][0]*self.N+roots[i][1]
            t=roots[i+1][0]*self.N+roots[i+1][1]
            self.edges[min(s,t)][max(s,t)]=1
        for s in range(len(square)//2-1):
            h,w,nh,nw=square[(2*s)%len(square)],square[(2*s+1)%len(square)],square[(2*s+2)%len(square)],square[(2*s+3)%len(square)]
            self.fields[h][w]=1
        
        return square
        
        
solver=Solver(fields)
#solver.search(13,24)
h=0
ans=[]
count=0
while time.time()-start_time<=1.5:
    h=(h+1)%N
    for w in range(N):
        if fields[h][w]==1:
            lr,ud,r_sheld,l_sheld=solver.search_box(h,w)
            squares=solver.generate(h,w,lr,ud,r_sheld,l_sheld)
            passed=[]
            for square in squares:
                passed=solver.check_edges(square)
            if passed:
                ans.append(passed)
                
    count+=1
#print(count)
print(len(ans))
for item in ans:
    print(*item)
