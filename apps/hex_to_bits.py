

data="00 00 00 00 00 4C 90 00 DE AD BE EF 00 54 68"
data=data.replace(" ","")

for i in range(len(data)/2):
    byte=int('0x'+data[i*2:i*2+2],16)
    for i in range(8):
        print str((byte>>(7-i))%2)+",",

