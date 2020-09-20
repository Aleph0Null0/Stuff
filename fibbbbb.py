def fibb(n):
    prev=1
    last=0
    for i in range(n):
        seq=prev+last
        print(seq,end=' ')
        last,prev=prev,seq

def fibrec(stop,n=1,f0=0):
    f1=n+f0
    if n>stop:
        return f1
    else:
        f0=n
        return fibrec(f1,n)

def fibsum(divrule=2,stop=4000000,n=1,f0=0,total=0):
    f1=n+f0
    if f1>stop:
        return total
    elif f1%divrule != 0:
        return fibsum(divrule,stop,f1,n,total)
    else:
        return fibsum(divrule,stop,f1,n,total+f1)
print(fibsum())