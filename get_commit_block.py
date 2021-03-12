import sys
import os

def endian_4(tmp):
    tmp1=tmp[2:4]
    tmp1+=tmp[0:2]
    return tmp1

def endian_8(tmp):
    tmp1 = tmp[7:9]
    tmp1 += tmp[5:7]
    tmp1 += tmp[2:4]
    tmp1 += tmp[:2]
    return tmp1


if len(sys.argv) !=2:
    print("Usage : sudo python3 get_commit_block.py %%FileSystem%%")
    print("example : sudo python3 get_commit_block.py /dev/sdb1")
    print("Must have sleuthkit installed... \"sudo apt install sleuthkit\"")
else:
    location = sys.argv[1]


#1-0 : Super Block (0ffset : 0x400)

off = 0x458
pay = 'xxd -l 0x10 -s '+str(hex(off))+' '+location
res = os.popen(pay).read()[10:19]
inode_size = int(endian_8(res),16)

off = 0x418
pay = 'xxd -l 0x10 -s '+str(hex(off))+' '+location
res = os.popen(pay).read()[10:19]
block_size=pow(2,int(endian_8(res),16)) * 0x400
print(hex(block_size))


#1-1 : Group Descriptor (offset : 0x1008~0x1009)
off = 0x1008
pay = 'xxd -l 0x10 -s '+str(hex(off))+' '+location
res = os.popen(pay).read()
inode = int(endian_4(res[10:15]),16)
print("inode no8(journal) offset : "+str(hex(inode)))

#1-2 : I-node table (offset 0x3c~0x3F)
off = 0x3C + inode*block_size+ 7*inode_size
pay = 'xxd -l 0x10 -s '+str(hex(off))+' '+location
res = os.popen(pay).read()[10:19]
jrnl = int(endian_8(res),16)*block_size


#1-3 : Read Commit Block Location
pay = 'jls -f ext4 '+location
res = os.popen(pay).read()
res =res.split('\n')
idx =[]
for i in range(len(res)):
    if 'Commit Block' in res[i]:
        num = res[i].split(':')[0]
        idx.append(int(num))

#1-4 : Read commit Block
for loc in idx:
    off = jrnl + loc*block_size
    pay = 'xxd -l 0x10 -s '+str(hex(off))+' '+location
    res = os.popen(pay).read()[:-1]
    print(res)
