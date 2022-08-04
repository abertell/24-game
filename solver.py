from math import log
from bisect import bisect_left as B
from collections import defaultdict as dd

BIG = 32
DIFF = 24
SMALL = 5e-3
ERR = 1e-12
special = (-1,0,1)

def eq(x,y):
    if x==None or y==None: return False
    if x in special or y in special: return x==y
    return abs(x-y)<ERR

def check(x):
    if x==None: return False
    rx = round(x)
    return eq(x,rx) or abs(x-rx)>SMALL

def wrap(f):
    def g(a,b):
        if a and b and abs(log(abs(a))-log(abs(b)))>DIFF: return None
        v = f(a,b)
        if v==None or check(v): return v
    return g

def wrapt(f):
    def g(a,b):
        if a and b and abs(log(abs(a))-log(abs(b)))>DIFF: return ()
        v = f(a,b)
        if v==() or check(v[0]): return v
        return ()
    return g

def op1(a,b): return a+b
def op2(a,b): return a-b
def op2R(a,b): return b-a
def op3(a,b): return a*b

def op4(a,b):
    if b==0: return None
    return a/b

def op4R(a,b): return op4(b,a)

def op5(a,b):
    rb = round(b)
    if not eq(b,rb): return None
    if rb==0 and b!=0: return None
    b = rb
    if a==0:
        if b>0: return 0
        return None
    if a==1 or b==0: return 1
    if a==-1: return -1 if b&1 else 1
    if b*log(abs(a))>BIG: return None
    v = a**b
    if v==0 or abs(v)==1: return None
    rv = round(v)
    if eq(v,rv):
        if abs(rv)<2: return None
        if abs(b)>1: return rv
    return v

def op5R(a,b): return op5(b,a)

anys = ["any","any-even"]

def ip1(a,b): return b-a,
def ip2(a,b): return a-b,
def ip2R(a,b): return a+b,

def ip3(a,b):
    if a==b==0: return "any",
    return op4(b,a),

def ip4(a,b):
    if a==0: return ()
    return op4(a,b),

def ip4R(a,b):
    if a==0: return ()
    return a*b,

def ip5(a,b):
    if b==1:
        if a==1: return "any",
        if a==-1: return "any-even",
        if a==0: return ()
        return 0,
    if b==-1: return ()
    if b>0:
        if a>0:
            v = op4(log(b),log(a))
            if v==None: return ()
            rv = round(v)
            if not eq(v,rv): return ()
            return rv,
        if a<0:
            v = op4(log(b),log(-a))
            if v==None: return ()
            rv = round(v)
            if not eq(v,rv) or rv&1: return ()
            return rv,
        return ()
    if b<0:
        if a<0:
            v = op4(log(-b),log(-a))
            if v==None: return ()
            rv = round(v)
            if not eq(v,rv) or rv-1&1: return ()
            return rv,
    return ()

def op5alt(b,a):
    e = op4(1,a)
    if e==None or e*log(abs(b))>BIG: return None
    v = b**e
    if v==0 or(abs(v)==1 and abs(b)!=1): return None
    rv = round(v)
    if eq(v,rv):
        if abs(rv)>1 and op5(rv,a)==b: return rv
        return None
    w = op5(v,a)
    if w and eq(w,b): return v

def ip5R(a,b):
    res = ()
    if b==1: res = 1,
    ra = round(a)
    if not eq(a,ra) or(ra==0 and a!=0): return res
    a = ra
    if b==1:
        if a-1&1: res = 1,-1
        return res
    if a==0: return ()
    if b==-1:
        if a&1: return -1,
        return ()
    if b==0: return ()
    if a==1: return b,
    if a==-1: return op4(1,b),
    if b>0:
        v = op5alt(b,a)
        if v==None: return ()
        if a&1 or v==0: return v,
        return v,-v
    if b<0:
        if a-1&1: return ()
        v = op5alt(-b,a)
        if v==None: return ()
        return -v,

class Op():
    def __init__(self,action,sym,rev):
        self.action = action
        self.sym = sym
        self.rev = rev
    def __call__(self,a,b):
        return self.action(a,b)
    def rep(self,a,b):
        if self.rev: return f'({b}{self.sym}{a})'
        return f'({a}{self.sym}{b})'

ops = [Op(op1,'+',0),Op(op2,'-',0),Op(op2R,'-',1),Op(op3,'*',0),Op(op4,'/',0),Op(op4R,'/',1),Op(op5,'**',0),Op(op5R,'**',1)]
ips = [Op(ip1,'+',0),Op(ip2,'-',0),Op(ip2R,'-',1),Op(ip3,'*',0),Op(ip4,'/',0),Op(ip4R,'/',1),Op(ip5,'**',0),Op(ip5R,'**',1)]
for op in ops: op.action = wrap(op.action)
for ip in ips: ip.action = wrapt(ip.action)

def comb(a,n,prefix=()):
    used = set()
    res = []
    for i in range(len(a)+1-n):
        v = a[i]
        if v not in used:
            used.add(v)
            if n==1: res.append(prefix+(v,))
            else: res+=comb(a[i+1:],n-1,prefix+(v,))
    return res

def flip(a,b):
    c = []
    j = 0
    for i in a:
        while j<len(b) and b[j]<i: j+=1
        if j<len(b) and b[j]==i: j+=1
        else: c.append(i)
    return tuple(c)

def preprocess(a):
    n = len(a)
    name = {}
    size = []
    orig = []
    comp = {}
    c = 0
    for i in range(1,n+1):
        for j in comb(a,i):
            name[j] = c
            orig.append(j)
            size.append(i)
            fwd = []
            back = []
            extra = []
            for x in range(1,(i>>1)+1):
                for y in comb(j,x):
                    f = flip(j,y)
                    if f==y:
                        extra = [name[y]]
                        continue
                    if x<i>>1 or name[y] not in back:
                        fwd.append(name[y])
                        back.append(name[f])
            comp[c] = tuple(fwd+extra+back[::-1])
            c+=1
    return comp,size,orig

def any_res(a):
    return '('+'+'.join(map(str,a))+')'

def even_res(a):
    n = len(a)
    for i in range(n):
        v = a[i]
        if v-1&1: return f'({v}**{any_res(a[:i]+a[i+1:])})'
    if n>2: return f'(({a[0]}+{a[1]})**{any_res(a[2:])})'
    if n==2: return any_res(a)

def solve(a,t,m=None):
    a = tuple(sorted(a))
    n = len(a)
    if n==1:
        if a[0]==t:
            print("Solution found")
            print(t)
            return 1
        print("No solution")
        return 0
    build = dd(list)
    rev = dd(list)
    if not m: m = (n>>1)+(n>6)
    comp,size,orig = preprocess(a)
    na = len(size)-1
    cflip = lambda a,b: comp[a][-1-comp[a].index(b)]
    x = px = 0
    while size[x]==1: build[x],x = list(orig[x]),x+1
    for i in range(2,m+1):
        print(f'Building at size {i}/{m}...')
        for j in range(px,x): build[j] = sorted(set(build[j]))
        px = x
        while size[x]==i:
            c = comp[x]
            lc = len(c)-(len(c)>>1)
            for j in range(lc):
                y = c[j]
                f = c[-1-j]
                for v1 in build[y]:
                    for v2 in build[f]:
                        for op in ops:
                            v = op(v1,v2)
                            if v!=None: build[x].append(v)
            x+=1
    for j in range(px,x): build[j] = sorted(set(build[j]))
    
    def btr(b,v):
        if size[b]==1: return f'{orig[b][0]}'
        c = comp[b]
        lc = len(c)-(len(c)>>1)
        for j in range(lc):
            y = c[j]
            f = c[-1-j]
            for vy in build[y]:
                for vf in build[f]:
                    for op in ops:
                        w = op(vy,vf)
                        if eq(w,v): return op.rep(btr(y,vy),btr(f,vf))
        return '???'
    
    def rtr(b,v):
        if b==na: return 'exp'
        b = cflip(na,b)
        c = (b,)+comp[b]
        for j in range(len(c)):
            y = c[j]
            x = cflip(na,c[-j]) if j else na
            for vy in build[y]:
                for vx in rev[x]:
                    for ip in ips:
                        r = ip(vy,vx)
                        for w in r:
                            if eq(w,v): return rtr(x,vx).replace('exp',ip.rep(btr(y,vy),'exp'))
        return '!!!'
    
    def run():
        nonlocal rev
        x = na
        nx = x-1
        rev[x] = [t]
        for i in range(n,m,-1):
            print(f'Reverse searching at size {i}/{m+1}...')
            for j in range(x,nx,-1): rev[j] = list(set(rev[j]))
            while size[x]==i:
                c = comp[x]
                lc = len(c)-(len(c)>>1)
                for j in range(lc):
                    y = c[j]
                    f = c[-1-j]
                    for v1 in build[y]:
                        for v2 in rev[x]:
                            for ip in ips:
                                r = ip(v1,v2)
                                for v in r:
                                    if v==None: continue
                                    if v in anys:
                                        if v=="any":
                                            w = any_res(orig[f])
                                            return 2,v1,y,v2,x,w,f,ip
                                        if v=="any-even":
                                            w = even_res(orig[f])
                                            if w: return 3,v1,y,v2,x,w,f,ip
                                    else:
                                        if size[f]>m: rev[f].append(v)
                                        else:
                                            bx = B(build[f],v)
                                            if bx<len(build[f]) and eq(build[f][bx],v): return 1,v1,y,v2,x,v,f,ip
                x-=1
            nx = x
            while size[nx]==i-1: nx-=1
        return 0,

    res = run()
    if res[0]==0:
        print("No solution")
        return 0
    print("Solution found")
    code,vy,y,ix,x,vf,f,ip = res
    sy = btr(y,vy)
    sx = rtr(x,ix)
    if code==1: sf = btr(f,vf)
    else: sf = vf
    print(sx.replace('exp',ip.rep(sy,sf))[1:-1])
    return 1

from random import *
def gen(n,la,ha,lt,ht):
    a = choices(range(la,ha),k=n)
    t = randrange(lt,ht)
    print(a,t)
    solve(a,t)
gen(8,1,10,100000,1000000)
