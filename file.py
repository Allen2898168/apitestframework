file1 = []
file2 = []
with open("dss订单号.txt", "r") as f:
    for i in f.readlines():
        line = i.strip('\n')
        file1.append(line)

with open("中间库订单号.txt", "r") as f:
    for i in f.readlines():
        line = i.strip('\n')
        file2.append(line)

err = []
for i in file1:
    if i in file2:
        pass
    else:
        err.append(i)
print("错误对不上的参数%s" % err)
