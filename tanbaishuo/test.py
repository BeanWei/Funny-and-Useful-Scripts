def genqq(qq):
    a=qq
    d = {"oe": 0, "n": 0, "z": 0, "on": 0,
         "oK": 1, "6": 1, "5": 1, "ov": 1,
         "ow": 2, "-": 2, "A": 2, "oc": 2,
         "oi": 3, "o": 3, "i": 3, "oz": 3,
         "7e": 4, "v": 4, "P": 4, "7n": 4,
         "7K": 5, "4": 5, "k": 5, "7v": 5,
         "7w": 6, "C": 6, "s": 6, "7c": 6,
         "7i": 7, "S": 7, "l": 7, "7z": 7,
         "Ne": 8, "c": 8, "F": 8, "Nn": 8,
         "NK": 9, "E": 9, "q": 9, "Nv": 9}
    l = 4
    ans = ''
    
    e=[]
    for j in [0,4,8,12,16,20]:
        e.append(qq[j:j+4])
    for k in range(len(e)):
        s=e[k]
        i = 0
        if s == None:
            break
        while (i <len(s) ):
            
            if i+1 < l:
                x = s[i]+s[i+1]
                if x in d.keys():
                    ans = ans+str(d[x])
                    i = i+2
                    
            if a[i] in d.keys() and i<len(s):
                ans = ans+str(d[s[i]])
                i = i+1
        k = k+1
    print(ans) 


testList = [
    "oKvPoK6kow6zNeEkNe6l7e-k",
    "oKvPoK6kow65oK6l7wosNe6q",
    "oKvPoK6kow65oKCkoi6ioK-F"
]

#"144115210895817425"
#"1440700315"

'''
144115210895817425
144115211117636819
144115211165313128
'''

'''
1441152
'''

for i in testList:
    genqq(i)
