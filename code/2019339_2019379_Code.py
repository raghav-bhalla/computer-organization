file  = open(r"C:\Users\ragha\Desktop\Inputfile.txt" ,'r')
symbolTable = {}
literalTable = {}

hlparr =[]
lc = 0
line = file.readline()


def removeComment(Line):
    global instr
    x = Line.find(';')
    y = Line.find('/')
    if x != -1:
        instr = Line[0:x]
    elif y != -1:
        instr = Line[0:y]
    else:
        instr = Line
    return instr

instruction = removeComment(line)
def checkLabel(instrt):
    x = instrt.find(':')
    if x != -1:
        return  instrt[0:x]
    else:
        return -1


def checkLiteral(s):
    if s.find("'") != -1:
        index_01 = s.index("'")
        index_02 = s.index("'", index_01 + 1)
        return s[index_01:index_02+1 ]

    else:
        return -1





with open(r"C:\Users\ragha\Desktop\Inputfile.txt",'r') as my_file:
    i = my_file.readlines()
    for j in i:
        if j=="END":
            break
        elif j=="CLA":
            lc+=1
        elif (j[:5] == "START"):
            lc = int(j[6::])
        else:
            cmnt = j.find(";")
            if cmnt != -1:
                j = j[:cmnt]
            if (len(j) != 0):
                if checkLabel(j)!=-1:
                    lab = checkLabel(j)
                    symbolTable[lab]=lc
                    hlparr.append([lab])
                elif checkLiteral(j) != -1:
                    lit = checkLiteral(j)
                    literalTable[lit] = lc
                    hlparr.append([lit])
                else:
                    x = j.find(" ")
                    sym = j[x+1:].strip()
                    symbolTable[sym] = lc
                    hlparr.append([sym])
            lc = lc+1

for x in hlparr:
            x.append((lc+1))
            lc +=1

if 'CLA' in symbolTable.keys():
    del symbolTable['CLA']

for q in hlparr:
    y  = q[1]
    y = str(format(y,'08b'))
    q[1] =y

for k in symbolTable.keys():
        for e in hlparr:
            if k==e[0]:
                symbolTable[k] = str((e[1]))

for k in literalTable.keys():
        for y in hlparr:
            if k==y[0]:
                literalTable[k] = str(y[1])

def labelNotFound(s,lc):
    if checkLabel(s)!=-1:
        lab = checkLabel(s)
        if lab in symbolTable.keys():
            return 0
        else:
            return -1
    else:
        return 0
def illegal_opcode(s,lc):
    opcodes=['START','CLA','LAC','SAC','ADD','SUB','BRZ','BRN','BRP','INP','DSP','MUL','DIV','END']
    if s[:3] in opcodes:
        return 0
    else:
        if s[:5]=='START':
            return 0
        else:
            return -1

def check_operands(s,lc):
    n = s.split()
    if n[0]=='START' or n[0]=='END':
        return 0
    if n[0]=='CLA' or n[0]=='STP':
        if len(n)!=1:
            if len(n)>1:
                return 1
            else:
                return 2
        else:
            return 0
    if n[0]=='DIV' or n[0]=='MUL' or n[0]=='DSP' or n[0]=='INP' or n[0]=='BRP' or n[0]=='BRN' or n[0]=='BRZ' or n[0]=='SUB' or n[0]=='ADD' or n[0]=='SAC' or n[0]=='LAC':
        if len(n)!=2:
            if len(n)>2:
                return 3
            else:
                return 4
        else:
            return 0

def second_pass():
    lc = 0
    opcodes = {'CLA': '0000', 'LAC': '0001', 'SAC': '0010', 'ADD': '0011', 'SUB': '0100', 'BRZ': '0101', 'BRN': '0110',
               'BRP': '0111', 'INP': '1000', 'DSP': '1001', 'MUL': '1010', 'DIV': '1011', 'STP': '1100'}
    with open(r"C:\Users\ragha\Desktop\Inputfile.txt", "r") as my_file01:
        j = my_file01.readlines()
    with open("text.txt", mode="w") as my_file_02:
        x=1
        y=0
        for i in j:
            e = i.find(':')
            if e!=-1:
                k = i[:e+1]
            cmnt = i.find(";")
            if cmnt != -1:
                i = i[:cmnt]
            if len(i)!=0:
                if (i[:5] == "START"):
                    lc = int(i[6::])
                if checkLabel(i)==-1:
                    if illegal_opcode(i,lc)==-1:
                        print("OPCODE NOT DEFINED ," + i + " " + str(lc))
                        print(i)
                        break
                if x==0:
                    print("START Error: Multiple Start statements found at, " +str(lc) )
                    break
                if check_operands(i,lc)!=0:
                    q = check_operands(i,lc)
                    if q==1 or q==3:
                        print("ERROR: Excess of operands found at, " + str(lc))
                    elif q==2 or q==4:
                        print("ERROR: Less no of operands found at, " + str(lc))
                    break
                if labelNotFound(i,lc)==-1:
                    print(i)
                    print("Label not found:error at, " + str(lc) )
                    break
                if i[:3]=='END':
                    lc = str(format(lc,'08b'))
                    my_file_02.write(str(lc))
                    my_file_02.write("   ")
                    my_file_02.write(opcodes["STP"])
                    my_file_02.write("   ")
                    my_file_02.write("00000000")
                    my_file_02.write("\n")
                    lc = int(lc, 2)
                if (i[:5] != "START" and i[:3] != "END"):
                    if i[:3] == "CLA":
                        lc = str(format(lc,'08b'))

                        my_file_02.write(str(lc))
                        my_file_02.write("   ")
                        my_file_02.write(opcodes["CLA"])
                        my_file_02.write("   ")
                        my_file_02.write("00000000")
                        my_file_02.write("\n")
                        lc = int(lc,2)

                    if checkLabel(i)!=-1:
                        lc = str(format(lc,'08b'))
                        y = i.find(':')
                        i=i[y+1::].strip()
                        operator = i[:3]
                        if operator=='STP' or operator=='END':
                            my_file_02.write(str(lc))
                            my_file_02.write("   ")
                            my_file_02.write(opcodes[operator])
                            my_file_02.write("   ")
                            my_file_02.write("00000000")
                            my_file_02.write("\n")
                            y=1
                            break

                        else:
                            add_op = opcodes[operator]
                            my_file_02.write(str(lc))
                            my_file_02.write("   ")
                            my_file_02.write(add_op)
                            my_file_02.write("   ")
                            temp = i[4::].strip()
                            if checkLiteral(temp)!=-1:
                                my_file_02.write((literalTable[temp]))
                                my_file_02.write("\n")

                            else:
                                my_file_02.write(symbolTable[temp])
                                my_file_02.write("\n")
                        lc = int(lc,2)
                    else:
                        lc = str(format(lc,'08b'))
                        operator = i[:3].strip()
                        add_op = opcodes[operator]
                        my_file_02.write(str(lc))
                        my_file_02.write("   ")
                        my_file_02.write(add_op)
                        my_file_02.write("   ")
                        temp = i[4::].strip()

                        if checkLiteral(temp)!=-1:
                            my_file_02.write((literalTable[temp]))
                            my_file_02.write("\n")

                        elif checkLabel(temp)!=-1:
                            my_file_02.write((symbolTable[temp]))
                            my_file_02.write("\n")

                        else:
                            my_file_02.write(symbolTable[temp])
                            my_file_02.write("\n")
                        lc = int(lc,2)

                    lc = lc + 1
    my_file_02.close()
print(symbolTable)
print(literalTable)
second_pass()
if y==0:
    print("ERROR:Endpoint Not Found")
else:
    with open("text.txt", "r") as f:
        for l in f:
            print(l.strip())










def labelNotFound(s,lc):
    if checkLabel()!=-1:
        lab = checkLabel(s)
        if lab in symbolTable.keys():
            return 0
        else:
            return -1
    else:
        return 0
