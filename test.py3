text = open("inputfile.txt","r").read()
start,end =0,0
data = []
temp = text.split()
for i in range(len(temp)):
    if temp[i] =="whenever" or temp[i]=="subroutine" or temp[i]=="from":
        start = i
    elif temp[i] == ';':
        end = i
        data.append(temp[:start])
        data.append(temp[start:end+1])
        data.append(temp[end+1:])
for i in data:
    print(i)