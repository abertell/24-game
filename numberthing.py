from math import log
from bisect import bisect_left as B

sop = ['+','-','*','/','**']
BIG = 99
INF = float('inf')
err = 1e-10
eq = lambda x,y: abs(x-y)<err

def op1(a,b):
    return a+b

def op2(a,b):
    return a-b

def op3(a,b):
    return a*b

def op4(a,b):
    if b==0: return None
    return a/b

def op5(a,b):
    if b!=int(b): return None
    b = int(b)
    if a==0:
        if b>0: return 0
        return None
    if a>0 and b*log(a)>BIG: return INF
    if a<0:
        if b&1 and b*log(-a)>BIG: return -INF
        if b-1&1 and b*log(-a)>BIG: return INF
    v = a**b
    rv = round(v)
    if rv and eq(v,rv): return rv
    return v

ops = [op1,op2,op3,op4,op5]

big = lambda x,y: x>y
small = lambda x,y: x<y
bigp = [big,small]
smallp = [small,big]
big5 = lambda x,y: not x or x>y
small5 = lambda x,y: not x or x<y
big5p = [big5,small5]
small5p = [small5,big5]
default = lambda x: 0
even = lambda x: x!=int(x) or int(x)&1
odd = lambda x: x!=int(x) or int(x)-1&1

def twp(L,H,Ls,Le,Hs,He,op,check,b,skip=default):
    xl,xh = Ls,Hs
    if xl==Le or xh==He: return 0
    Ldir = 1 if Le>Ls else -1
    Hdir = 1 if He>Hs else -1
    while True:
        if op(L[xl],H[xh])==b: return L[xl],H[xh]
        while xh!=He and (check[0](op(L[xl],H[xh]),b) or skip(H[xh])): xh+=Hdir
        if xh==He: break
        if op(L[xl],H[xh])==b: return L[xl],H[xh]
        while xl!=Le and check[1](op(L[xl],H[xh]),b): xl+=Ldir
        if xl==Le: break
    return 0

def p1(L,H,b):
    return twp(L,H,0,len(L),len(H)-1,-1,op1,bigp,b)

def p2(L,H,b):
    return twp(L,H,0,len(L),0,len(H),op2,bigp,b)

def p3(L,H,b):
    L0,H0 = B(L,0),B(H,0)
    if b>0:
        return(twp(L,H,0,L0,H0-1,-1,op3,smallp,b) or
               twp(L,H,L0,len(L),len(H)-1,H0-1,op3,bigp,b))
    if b<0:
        return(twp(L,H,0,L0,H0,len(H),op3,bigp,b) or
               twp(L,H,L0,len(L),0,H0,op3,smallp,b))
    if L0<len(L) and H0<len(H) and op3(L[L0],H[H0])==0: return L[L0],H[H0]
    return 0

def p4(L,H,b):
    L0,H0 = B(L,0),B(H,0)
    if b>0:
        return(twp(L,H,0,L0,0,H0,op4,smallp,b) or
               twp(L,H,L0,len(L),H0,len(H),op4,bigp,b))
    if b<0:
        return(twp(L,H,0,L0,len(H)-1,H0-1,op4,bigp,b) or
               twp(L,H,L0,len(L),0,H0,op4,smallp,b))
    if L0<len(L) and H0<len(H) and op4(L[L0],H[H0])==0: return L[L0],H[H0]
    return 0

def p5(L,H,b):
    Ln1,L1 = B(L,-1),B(L,1)
    L0,H0 = B(L,0),B(H,0)
    if b>1:
        return(twp(L,H,0,Ln1,H0,len(H),op5,small5p,b,even) or
               twp(L,H,Ln1,L0,0,H0,op5,big5p,b,even) or
               twp(L,H,L0,L1,H0-1,-1,op5,small5p,b) or
               twp(L,H,L1,len(L),len(H)-1,H0-1,op5,big5p,b))
    if b<-1:
        return(twp(L,H,0,Ln1,H0,len(H),op5,big5p,b,odd) or
               twp(L,H,Ln1,L0,0,H0,op5,small5p,b,odd))
    if 0<b<1:
        return(twp(L,H,0,Ln1,H0-1,-1,op5,big5p,b,even) or
               twp(L,H,Ln1,L0,len(H)-1,H0-1,op5,small5p,b,even) or
               twp(L,H,L0,L1,H0,len(H),op5,big5p,b) or
               twp(L,H,L1,len(L),0,H0,op5,small5p,b))
    if -1<b<0:
        return(twp(L,H,0,Ln1,H0-1,-1,op5,small5p,b,odd) or
               twp(L,H,Ln1,L0,len(H)-1,H0-1,op5,big5p,b,odd))
    if b==1:
        if L1<len(L) and H0<len(H) and (L[L1]==1 or H[H0]==0): return L[L1],H[H0]
        if Ln1<len(L) and L[Ln1]==-1:
            for h in H:
                if h==int(h) and h-1&1: return L[Ln1],h
        return 0
    if b==-1:
        if Ln1<len(L) and L[Ln1]==-1:
            for h in H:
                if h==int(h) and h&1: return L[Ln1],h
        return 0
    if L0<len(L) and L[L0]==0:
        for h in H:
            if h!=0: return L[Ln1],h
    return 0

ps = [p1,p2,p3,p4,p5]

def fast(a,b,top=0):
    n = len(a)
    if n==1: return a
    A = []
    for i in range(n-1):
        L = fast(a[:i+1],b)
        H = fast(a[i+1:],b)
        if not top:
            for v1 in L:
                for v2 in H:
                    for op in ops:
                        v = op(v1,v2)
                        if v and abs(v)!=INF: A.append(v)
            continue
        if (not L) or (not H): continue
        L = sorted(set(L))
        H = sorted(set(H))
        for j in range(5):
            ans = ps[j](L,H,b)
            if ans: return i,j,ans[0],ans[1]
    if not top: return A
    return 0

def perms(a):
    if len(a)==1: return [a]
    r = []
    used = set()
    for i in range(len(a)):
        if a[i] not in used:
            used.add(a[i])
            for j in perms(a[:i]+a[i+1:]): r.append((a[i],)+j)
    return r

def solve(a,b,back=0):
    n = len(a)
    if back: P = [a]
    else: P = perms(tuple(a))
    c = r = 0
    N = len(P)
    div = ([1]*6 + [10,100,1000])[n]
    for ns in P:
        if not back and n>7: print(ns)
        v = (c*div)//N
        if not back and v>r:
            r = v
            print(f'{r*100/div:.1f}%')
        c+=1
        if back and n==1: return f'{a[0]}'
        ans = fast(ns,b,1)
        if ans:
            if not back: print("Solution found")
            i,j,l,r = ans
            ls = solve(ns[:i+1],l,back=1)
            rs = solve(ns[i+1:],r,back=1)
            s = '('+ls+sop[j]+rs+')'
            if back: return s
            print(s[1:-1])
            return 1
    return 0

# EXAMPLE
solve([2,3,4,5,6,7],8901)
