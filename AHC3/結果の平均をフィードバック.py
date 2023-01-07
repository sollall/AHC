# coding: utf-8
# Your code here!
import time
import sys
import heapq as hq

sys.setrecursionlimit(1000000) #上限を１００万回に設定

class Solver:
    def __init__(self,N):       
        self.N=N
        self.maze=[[1 for i in range(self.N)] for j in range(self.N)]


        self.edge=[{} for i in range(self.N*self.N)]
        
        
        self.ans=""
        self.topcost=0
        self.limit=0.1
        
        self.init_cost=1
        for h in range(self.N):
            for w in range(self.N):
                pos=self.xy2hash(w,h)
                if pos//self.N!=0:
                    self.edge[pos][pos-self.N]={"cost":self.init_cost,"count":1}
                if pos//self.N!=self.N-1:
                    self.edge[pos][pos+self.N]={"cost":self.init_cost,"count":1}
                if pos%self.N!=0:
                    self.edge[pos][pos-1]={"cost":self.init_cost,"count":1}
                if pos%self.N!=self.N-1:
                    self.edge[pos][pos+1]={"cost":self.init_cost,"count":1}
    
    def solve(self,sx,sy,tx,ty):
        self.start=time.time()
        self.visited=[10**9 for i in range(self.N*self.N)]
        self.q=[ [ 0,self.xy2hash(sx,sy),[self.xy2hash(sx,sy)] ] ]
        hq.heapify(self.q)

        while self.q:
            cost,now,way=self.bfs(hq.heappop(self.q))
            #print(cost,now,way)
            if ty==now//self.N and tx==now%self.N:
                break
        if len(self.q)==0:
            print("たどり着かないの草")
            
        #wayから移動票を作成する
        ans=self.generate_answer(way)
        print(ans)
        
        #答えを受け取ってフィードバックする
        #result=int(input())
        #self.feedback(result,way)
        
        return 

    def xy2hash(self,x,y):
        return y*self.N+x

    def evaluate(self,num):
        x,y=num%self.N,num//self.N

        return min(x,self.N-1-x)**2+min(y,self.N-1-y)**2

    def bfs(self,content):
        cost,now,way=content
        #print(content,self.edge[now])
        for nxt,item in self.edge[now].items():
            #行先を4つ生成して飛べばedgeの数を減らせる
            way_cost,way_count=item["cost"],item["count"]
            if self.visited[nxt]>cost+way_cost:
                self.visited[nxt]=cost+way_cost
                hq.heappush(self.q,[cost+way_cost/way_count,nxt,way+[nxt]])

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
                rev+="R"#"R"
        return rev
                
    def feedback(self,all_cost,way):
        avg=all_cost/(len(way)-1)
        for i in range(len(way)-1):
            self.edge[way[i]][way[i+1]]["cost"]+=avg
            self.edge[way[i+1]][way[i]]["cost"]+=avg
            self.edge[way[i]][way[i+1]]["count"]+=1
            self.edge[way[i+1]][way[i]]["count"]+=1        
            
        return 
        


solver=Solver(30)

for _ in range(1000):
    sy,sx,ty,tx=map(int,input().split())
    solver.solve(sx,sy,tx,ty)

    