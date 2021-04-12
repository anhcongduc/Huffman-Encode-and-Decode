from bitarray import bitarray
import time
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
    for i in read:
        i = i.split("'],")
        i = i[0]
        i = i.split(", '")
        i[0]=int(i[0])
        read1.append(i)
    return read1
a=input("nhap ten file: ")
time_start_encode=time.time()
list=open(a,"rb")#doc file
tenfile=list.name#lay name file
duoifile=tenfile[len(tenfile)-4:]
tenfile=tenfile[:len(tenfile)-4]#lay ten file input
readbit=bitarray()
readbit.fromfile(list)
readbit=readbit.tobytes()
list=""
for i in readbit:
    list=list+chr(i)
ex=list#tao ban sao cua file da doc
i=0
list1,list2=[],[]#lis1 luu ky tu va so lan xuat hien,list 2 luu so lan xuat hien
""" dem ky tu va so lan xuat hien cua ky tu """
while(i<256):
    a=chr(i)
    b=list.count(a)
    if(b>0):
        list1.append(a)
        list1.append(b)
        list2.append(b)
    i=i+1
list3=[]#tao list luu ky tu
list2.sort()
for i in list2:# sap xep ky tu va so lan xuat hien tang dan
    list3.append(list1[list1.index(i)-1])
    list1.remove(list1[list1.index(i)])
codes={}#khai bao dict codes
for i in list3:#tao cac key cua dict codes
    codes[i]=0
#tao list thich hop de tao cay huffman
i=0
list=list3[0:2]
listex=[]
while(i<len(list2)):
    flag=[]
    flag.append(list2[i])
    flag.append(list3[i])
    listex.append(flag)
    i=i+1
cuttree=createhuffmantree(listex)
write1=open(tenfile+"solanxuathien"+duoifile,"w")
write=open(tenfile+"kytu"+duoifile,"wb")
print(len(listex))
listex1=""
for i in listex:
   write1.write(str(i[0]))
   write1.write("\n")
   a=ord(i[1])
   a=get8bit(a)
   listex1+=a
write1.close()
listex1=bitarray(listex1)
write.write(listex1)
write.close()
assignCodes(cuttree)#tu cay tao dictionary codes de de dang encode trong buoc tiep theo
encoded=encode(ex)#goi ham encode van ban da cho voi ex la ban sao cua van ban da doc vao
time_end_encode=time.time()
print("thoi gian nen la: ",round(time_end_encode-time_start_encode,2))
time_start_ghifile=time.time()
#ghi ra file tenfile+encode
writebin=open(tenfile+"encode"+duoifile,"wb")
encoded=bitarray(encoded)
writebin.write(encoded)
time_end_ghifile=time.time()
print("Thoi gian ghi ra file encode la: ",round(time_end_ghifile-time_start_ghifile,2))
