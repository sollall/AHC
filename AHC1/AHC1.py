# coding: utf-8
# Your code here!
import random
import time

class Ad_map:
    def __init__(self,N,pos):
        self.pos=pos
        self.N=N
        self.ad_map=[]
        self.happies=[]
        for i,(x,y,r) in enumerate(pos):
            self.ad_map.append([x,y,x+1,y+1])
            self.happies.append(self.calc_happy([x,y,x+1,y+1],r))
            
    def calc_happy(self,position,r):
        x1,y1,x2,y2=position
        s=(x2-x1)*(y2-y1)
        return 1-(1-min(s,r)/max(s,r))**2
    
    def sampling(self):
        #randomに選ぶ
        target=random.randint(0,self.N-1)

        #大きくする　0→左に拡張 1→上に拡張 2→右に拡張 3→下に拡張
        x1,y1,x2,y2=self.ad_map[target]
        dire=random.randint(0,3)
        if dire==0:
            new_pos=[x1-1,y1,x2,y2]
        elif dire==1:
            new_pos=[x1,y1-1,x2,y2]
        elif dire==2:
            new_pos=[x1,y1,x2+1,y2]
        elif dire==3:
            new_pos=[x1,y1,x2,y2+1]
        
        if self.check_over(target,new_pos) and self.check_overrange(target,new_pos):
            r=self.pos[target][2]
            if self.calc_happy(new_pos,r)>self.happies[target]:
                self.ad_map[target]=new_pos
                self.happies[target]=self.calc_happy(new_pos,r)
                #print("成功")
            else:
                print("幸福度があがらない")
                pass
        else:
            #print("要件に合わない")
            pass
            
        return 
    
    #checkすること　重なってないかはみだしてないか本来の中心を逃してないか
    """
    def check_over(self,number,position):
        rev=True
        xx1,yy1,xx2,yy2=position
        for n in range(self.N):
            if number==n:#自分自身はスキップ
                continue
            else:
                x1,y1,x2,y2=self.ad_map[n]
                #numの広告のx1,y1がnの広告のx1,y1とx2,y2の間にないか
                for x,y in [[xx1,yy1],[xx1,yy2],[xx2,yy1],[xx2,yy2]]:
                    if x1<x and x<x2 and y1<y and y<y2:
                        rev=False
        return rev
    """
    #新しいpositionが他と重ならないかチェックする
    def check_over(self,number,a):#positionを二つ
        ax1,ay1,ax2,ay2=a
        rev=True

        for n in range(self.N):
            if number==n:#自分自身はスキップ
                continue
            else:
                bx1,by1,bx2,by2=self.ad_map[n]
                mid_a=(ax1+ax2)/2,(ay1+ay2)/2
                mid_b=(bx1+bx2)/2,(by1+by2)/2
                
                width_a=abs(ax2-ax1)
                height_a=abs(ay2-ay1)
                
                width_b=abs(bx2-bx1)
                height_b=abs(by2-by1)
        
                if abs(mid_a[0]-mid_b[0])<(width_a+width_b)/2 and abs(mid_a[1]-mid_b[1])<(height_a+height_b)/2:
                    rev=False

        return rev

    def check_overrange(self,num,position):
        if -1 in position or 10**4+1 in position:
            return False
        else:
            return True
    
    def answer(self):
        for ad in self.ad_map:
            print(*ad)
        return 


n=int(input())
limit=4.8

pos=[]
for _ in range(n):
    x,y,r=map(int,input().split())
    pos.append([x,y,r])
    
test=Ad_map(n,pos)

start=time.time()
while time.time()-start<limit:
    test.sampling()

print("----------------------")
test.answer()
