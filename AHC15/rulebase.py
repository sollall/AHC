A = list(map(lambda x: int(x)-1, input().split()))
for v, nv in zip(A, A[1:]):
  print("F" if not nv else "B" if not v else "L" if nv < 2 else "R")