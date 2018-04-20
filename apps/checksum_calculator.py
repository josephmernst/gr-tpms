import sys


def usage():
    print "python checksum_calculator.py DATA"
    print "Examples:"
    print "python checksum_calculator.py 00000000004C900070B5948D0042"
    print """python checksum_calculator.py "00 00 00 00 00 4C 90 00 70 B5 94 8D 00 42 64" """

if __name__=='__main__':
    print len(sys.argv)
    if len(sys.argv)!=2:
        usage()
        sys.exit(-1)

    data_in=sys.argv[1]

    data=data_in.replace(" ","")
    print data
    if len(data) != 32:
        raise Exception("length of data should be 28.  Current length is %d"%len(data))
        
    checksum=0
    for i in range(len(data)/2):
        byte=int('0x'+data[i*2:i*2+2],16)
        checksum+=byte

    print "checksum: %02X"%(checksum&0xFF)


