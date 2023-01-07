# coding: utf-8
# Your code here!
#import time
import heapq as hq
from sklearn.linear_model import Ridge
import numpy as np
import random 


class Solver:
    def __init__(self,N):
        #self.ts=time.time()
        
        self.N=N

        self.ans=""
        self.topcost=0
        self.limit=0.1
        
        self.init_cost=50
        
        self.X=np.zeros((1,3480//2))
        self.y=np.zeros((1,1))
        
        self.edge=[{} for i in range(self.N*self.N)]
        for h in range(self.N):
            for w in range(self.N):
                pos=self.xy2hash(w,h)
                #if pos//self.N!=0:
                #    self.edge[pos][pos-self.N]=self.init_cost                
                if pos//self.N!=self.N-1:
                    self.edge[pos][pos+self.N]=self.init_cost              
                #if pos%self.N!=0:
                #    self.edge[pos][pos-1]=self.init_cost           
                if pos%self.N!=self.N-1:
                    self.edge[pos][pos+1]=self.init_cost

        #self.edge_bfs=[{} for i in range(self.N*self.N)]
        self.edge_bfs=[[] for i in range(self.N*self.N)]
        for h in range(self.N):
            for w in range(self.N):
                pos=self.xy2hash(w,h)
                if pos//self.N!=0:
                    #self.edge_bfs[pos][pos-self.N]=self.init_cost
                    self.edge_bfs[pos].append(pos-self.N)
                if pos//self.N!=self.N-1:
                    self.edge_bfs[pos].append(pos+self.N)
                if pos%self.N!=0:
                    self.edge_bfs[pos].append(pos-1)
                if pos%self.N!=self.N-1:
                    self.edge_bfs[pos].append(pos+1)
                    
        #print(time.time()-self.ts)

    def solve(self,sx,sy,tx,ty,count):
        #self.start=time.time()
        self.visited=[10**9 for i in range(self.N*self.N)]
        self.q=[ [ 0,self.xy2hash(sx,sy),[self.xy2hash(sx,sy)] ] ]
        hq.heapify(self.q)
        
        #print(1,time.time()-self.ts)

        while self.q:
            cost,now,way=self.bfs(hq.heappop(self.q))
            if ty==now//self.N and tx==now%self.N:
                break
        
        #print(2,time.time()-self.ts)
        #wayから移動票を作成する
        ans=self.generate_answer(way)
        print(ans)

        #答えを受け取ってフィードバックする
        result=int(input())
        
        if count%50==0:
            self.feedback(result,way)
        else:
            pass

        return 

    def xy2hash(self,x,y):
        return y*self.N+x

    def bfs(self,content):
        cost,now,way=content
        
        for _,nxt in enumerate(self.edge_bfs[now]):
            way_cost=self.edge[min(now,nxt)][max(now,nxt)]
            if self.visited[nxt]>cost+way_cost:
                self.visited[nxt]=cost+way_cost
                hq.heappush(self.q,[cost+way_cost,nxt,way+[nxt]])
        
        return content
    
    def generate_answer(self,way):
        rev=""
        for i in range(len(way)-1):
            if way[i+1]//self.N-way[i]//self.N==-1:
                rev+="U"#U
            elif way[i+1]//self.N-way[i]//self.N==1:
                rev+="D"
            elif way[i+1]%self.N-way[i]%self.N==-1:
                rev+="L"    
            elif way[i+1]%self.N-way[i]%self.N==1:
                rev+="R"
        return rev
                
    def feedback(self,all_cost,way):
        use_edge=[{} for i in range(self.N*self.N)]
        #wayから使用したedgeを調べる
        #まずwayから使った道を抜き出して、for文で順番に調べて存在したらbitを立てるどうか
        for i in range(len(way)-1):
            _min,_max=min(way[i],way[i+1]),max(way[i],way[i+1])
            use_edge[_min][_max]=1

        #startと#
        #temp_x内の順序と
        
        #temp_x=np.arange(0)
        
        
        temp_x=[]
        order=[]
        for pos in range(self.N*self.N):
            for npos in self.edge[pos]:
                if npos in use_edge[pos]:
                    #temp_x=np.append(temp_x,[1])
                    temp_x.append(1)
                    order.append([pos,npos])
                else:
                    #temp_x=np.append(temp_x,[0])
                    temp_x.append(0)
                    order.append([pos,npos])
        temp_x=np.array(temp_x)

    
        self.X=np.vstack((self.X,temp_x))
        self.y=np.append(self.y,[all_cost])

        #ridge回帰して係数を得る　これを次の
        ridge = Ridge().fit(self.X, self.y)
        
        
        for i in range(len(order)):
            pred_cost=ridge.coef_[i]
            p1,p2=order[i]
            self.edge[p1][p2]=pred_cost
            
        return 
        

solver=Solver(30)

for iter in range(1000):
    sy,sx,ty,tx=map(int,input().split())
    solver.solve(sx,sy,tx,ty,iter)

    