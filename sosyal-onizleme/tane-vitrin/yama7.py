import sys
p=sys.argv[1];t=open(p,encoding='utf-8').read()
a="const wr=(x,y)=>0.008*Math.sin(x*21+y*13)*Math.sin(y*29-x*9)+0.004*Math.sin(x*57-y*41);"
b="const wr=(x,y)=>0.007*Math.sin(x*5.3+y*2.1+1.3)*Math.sin(y*3.7-x*1.9)+0.003*Math.sin(x*9.1+Math.sin(y*6.3)*1.7);"
assert a in t;t=t.replace(a,b)
open(p,'w',encoding='utf-8').write(t);print('tamam')
