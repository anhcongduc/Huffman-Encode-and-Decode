import time
from bitarray import bitarray
def buildtree(list):# ham tao cay huffman tu data da co sap xep tang dan
    while(len(list)>1):
        listtwo=list[0:2]
        therest=list[2:]
        combfreq=listtwo[0][0]+listtwo[1][0]
        list=therest+[(combfreq,listtwo)]
    return list[0]
def cuttreee(tree):#ham cat bot so lan xuat hien cua ki tu
    p=tree[1]
    if type(p)==type(""): return p
    else: return(cuttreee(p[0]),cuttreee(p[1]))
def assignCodes(node,pat=''):#ham encode tung ky tu xuat hien trong van ban tu cay ma huffman va luu vao dict codes voi key la ky tu
    global codes
    if type(node)==type(""):
        codes[node]=pat
    else:
        assignCodes(node[0],pat+"0")
        assignCodes(node[1],pat+"1")
def encode(str):#ham encode van ban thanh ma nhi phan theo dict codes da co
    global codes
    output=""
    for ch in str:
        output += codes[ch]
    return output
def decode (tree, str) :#ham giai ma tu cay ma va chuoi nhi phan da encode
    output = ""
    p = tree
    for bit in str :
        if bit == '0' : p = p[0]
        else          : p = p[1]
        if type(p) == type("") :
            output += p
            p = tree
    return output
def getint(a):#chuyen chuoi chua cac nhi phan thanh int duoi dang thap phan
    i=7
    getintt=0
    for flag in a:
        getintt+=int(flag)*pow(2,i)
        i=i-1
    return getintt
def getlist(encoded):# tao list cac so nguyen tu day bit da encode
    listoutput = []
    while(len(encoded)!=0):
        if (len(encoded) >= 8):
            a = encoded[:8]
            a = getint(a)
            encoded = encoded[8:]
            listoutput.append(a)
        else:
            a = encoded
            a = getint(a)
            list.append(a)
            encoded=""
    return listoutput
def get8bit(a):#chuyen int thanh nhi phan 8 bit de decode
    if(a>=128):
        b=bin(a)[2:]
        return b
    else:
        b=bin(a)[2:]
        while(len(b)<8):
            b="0"+b
        return b
def decodefromfile(readfile):#tao lai string ma nhi phan tu file da nen
    result=""
    for i in readfile:
        a=get8bit(i)
        result+=a
    return result
def createhuffmantree(listex):#ham tao cay huffman tu list luu ky tu va so lan xuat hien
    tree = buildtree(listex)  ##goi ham tao cay
    tree = cuttreee(tree) # cay cat di chi so
    return tree
def gethuffmanlist(read):
    read = read[2:len(read) - 3]
    read = read.split("[")
    read1 = []
    print(read[1])
    for i in read:
        print(i)
        i = i.split("'],")
        print(i)
        i = i[0]
        i = i.split(", '")
        i[0]=int(i[0])
        read1.append(i)
    return read1
a=input("nhap ten file decode: ")
b=input("nhap duoi file dau ra decode: ")
print("decode tu file!!!!")
time_start_decode=time.time()
readhuffmankytu=open(a+"kytu"+b,"rb")
readhuffmansolanxuathien=open(a+"solanxuathien"+b,"r",encoding="cp1252")
readhuffmansolanxuathien=readhuffmansolanxuathien.readlines()
for i in range(len(readhuffmansolanxuathien)):
    readhuffmansolanxuathien[i]=readhuffmansolanxuathien[i].replace("\n","")
huffmanlist=bitarray()
huffmanlist.fromfile(readhuffmankytu)
huffmanlist1=[]
while(len(huffmanlist)>0):
    solan=getint(huffmanlist[:8])
    solan=chr(solan)
    huffmanlist1.append([readhuffmansolanxuathien[0],solan])
    readhuffmansolanxuathien=readhuffmansolanxuathien[1:]
    huffmanlist=huffmanlist[8:]
decodetree=createhuffmantree(huffmanlist1)
readfile=open(a+"encode"+b,"rb")
readfile=readfile.read()
encoded2=decodefromfile(readfile)##goi ham decode tu file chuyen thanh string luu cac bit
decoded=decode(decodetree,encoded2)#goi ham decode tu cay ma huffman va string luu cac bit
time_end_decode=time.time()
print("thoi gian decode la:",round(time_end_decode-time_start_decode,2))
write=open(a+"decode"+b,"wb")
decoded1=""
for i in decoded:
    i=ord(i)
    a=get8bit(i)
    decoded1+=a
decoded1=bitarray(decoded1)
write.write(decoded1)

