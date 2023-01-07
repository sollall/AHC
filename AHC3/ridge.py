# coding: utf-8
# Your code here!
#import time
import heapq as hq
import numpy as np
import time

class MyRidgeRegressor:
    def __init__(self, alpha=1.0):
        self.alpha = float(alpha) # ←New!!
        self.dim = None
        self.coef_ = None
        self.intercept_ = None
        self.n_feature = None
        self.__name__ = "Ridge"

    def fit(self, X, y, dim=1):
        n_sample, n_feature = X.shape
        # X (n_sample, dim, n_feature)
        X = np.array([[x**i for i in range(dim + 1)] for x in X])
        # delete duplicated ones array
        #X = X.reshape(n_sample, -1)[:, n_feature - 1:]
        X = X.reshape(n_sample, -1)[:, n_feature-1:]
        # define identity matrix
        eye = np.eye(n_feature+1 ) # ←New!!
        # calculate coefficient
        weight = np.dot(np.dot(np.linalg.inv(np.dot(X.T, X) + self.alpha * eye), X.T), y) # ←New!!
        self.coef_ = weight[ 1:]
        self.intercept_ = weight[0]
        self.dim = dim
        self.n_feature = n_feature


class Solver:
    def __init__(self,N):
        #self.ts=time.time()
        
        self.N=N

        self.ans=""
        self.topcost=0
        self.limit=0.1
        
        self.init_cost=50
        
        #縦方向*列のway,横方向*行のwayで60
        self.X=np.zeros((1,30*2))
        self.y=np.zeros((1,1))
        self.ridge=MyRidgeRegressor()
        
        self.way_costs=[self.init_cost]*60
        
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

    def solve(self,sx,sy,tx,ty,count):
        
        self.visited=[10**9 for i in range(self.N*self.N)]
        self.q=[ [ 0,self.xy2hash(sx,sy),[self.xy2hash(sx,sy)] ] ]
        hq.heapify(self.q)

        while self.q:
            cost,now,way=self.bfs(hq.heappop(self.q))
            if ty==now//self.N and tx==now%self.N:
                break
        
        #wayから移動票を作成する
        ans=self.generate_answer(way)
        print(ans)

        #答えを受け取ってフィードバックする
        result=int(input())
        
        if count<=30:
            self.feedback(result,way)
        else:
            pass

        return 

    def xy2hash(self,x,y):
        return y*self.N+x

    def evaluate(self,num):
        x,y=num%self.N,num//self.N

        return min(x,self.N-1-x)**2+min(y,self.N-1-y)**2

    def bfs(self,content):
        cost,now,way=content
        
        for _,nxt in enumerate(self.edge_bfs[now]):
            tmp_pos=min(nxt,now)
            if abs(nxt-now)==1:
                #横方向→高さが欲しい
                way_cost=self.way_costs[tmp_pos//self.N]
            else:
                way_cost=self.way_costs[self.N+tmp_pos%self.N]
            
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
        use_edge=[0]*60
        #横方向のwayなら0+h,縦方向なら30+w
        log=time.time()
        
        for i in range(len(way)-1):
            _min,_max=min(way[i],way[i+1]),max(way[i],way[i+1])
            if _max-_min==1:
                use_edge[_min//self.N]+=1
            else:
                use_edge[self.N+_min%self.N]+=1

        self.X=np.vstack((self.X,use_edge))
        self.y=np.append(self.y,[all_cost])

        #ridge回帰して係数を得る　これを次の
        self.ridge.fit(self.X, self.y)
        self.way_costs=self.ridge.coef_[:]
        self.way_costs=[max(item,0.1) for item in self.way_costs]

        return 
        

solver=Solver(30)

log=time.time()
for iter in range(1000):
    sy,sx,ty,tx=map(int,input().split())
    solver.solve(sx,sy,tx,ty,iter)
