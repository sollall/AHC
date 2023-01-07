# coding: utf-8
# Your code here!
import time
import sys

sys.setrecursionlimit(1000000) #上限を１００万回に設定

class Solver:
    def __init__(self,maze,price):
        self.maze=maze
        self.price=price
        
        self.N=len(maze)
        
        self.edge=[{} for i in range(self.N*self.N)]
        self.visited=[0 for i in range(self.N*self.N)]
        
        self.ans=""
        self.topcost=0
        self.limit=1.9
        
        for h in range(self.N):
            for w in range(self.N):
                pos=h*self.N+w
                if pos//self.N!=0:
                    self.edge[pos][pos-self.N]=1
                if pos//self.N!=self.N-1:
                    self.edge[pos][pos+self.N]=1
                if pos%self.N!=0:
                    self.edge[pos][pos-1]=1
                if pos%self.N!=self.N-1:
                    self.edge[pos][pos+1]=1
    
    def solve(self,sx,sy):
        self.start=time.time()
        self.dfs(sx*self.N+sy,0,"")
        
        return 

    def dfs(self,pos,cost,way):#visitedも渡さないといけない？だるい
        uniq=self.maze[pos//self.N][pos%self.N]
        #答えを記録
        if time.time()-self.start>self.limit:
            print(self.ans)
            exit()
        else:
            if self.topcost<cost:
                self.ans=way
                self.topcost=cost
        
        h,w=pos//self.N,pos%self.N
        uniq=self.maze[h][w]
        self.visited[uniq]=1
        
        #行先選定
        target=[]
        new_pos=[]
        
        if h!=0:
            new_pos.append([w,h-1])
        if w!=0:
            new_pos.append([w-1,h])
        if h!=self.N-1:
            new_pos.append([w,h+1])
        if w!=self.N-1:
            new_pos.append([w+1,h])
        
        for x,y in new_pos:
            nuniq=self.maze[y][x]
            
            if self.visited[nuniq]:
                continue
            else:
                target.append(y*self.N+x)
        """
        for key,e in self.edge[pos].items():
            nh,nw=key//self.N,key%self.N
            nuniq=self.maze[nh][nw]
            
            if self.visited[nuniq]:
                continue
            else:
                target.append(key)
        """     
                
        #遷移する
        
        for t in target:
            dire=""
            if (t//self.N-pos//self.N)==1:
                dire="D"
            elif (t//self.N-pos//self.N)==-1:
                dire="U"
            elif (t%self.N-pos%self.N)==1:
                dire="R"
            elif (t%self.N-pos%self.N)==-1:
                dire="L"
            else:
                print("ばぐ")
                exit()
            
            self.dfs(t,cost+self.price[h][w],way+dire)
        
        #復元処理
        self.visited[self.maze[h][w]]=0
        return target
        

sx,sy=map(int,input().split())
RANGE=50

m=[]
p=[]
for _ in range(RANGE):
    m.append(list(map(int,input().split())))

for _ in range(RANGE):
    p.append(list(map(int,input().split())))

solver=Solver(m,p)

solver.solve(sx,sy)
