import math 
code = open('code.asm', 'r')
symbolFile = open("SymTab.txt" , "w") 
interMedite = open("INTMD.mdt" , "w")
errorList = open("error.txt" , "w")
opcode = open("OPTAB.txt")
optab = {}
symTab = {}
literals ={} # using literals to prevent duplication 

#reading OPTABLE from OPTAB.txt file and store them in a dictionary
while True:
    line = opcode.readline()
    if not line:
        break
    op = line[0:11].strip()
    opnum = line[11:13].strip()
    optab.update({op : opnum})

# reading the name of the progrm 
line = code.readline()
progName = line[0:10].strip()
initialLOCCTR = hex(int(line[21:39].strip(),16))
LOCCTR = initialLOCCTR
interMedite.write(str(LOCCTR[2:]) +"      "+ line)


while True:
    line = code.readline()
    if not line:
        break
    if (line[11:20].strip() == "END"):
        interMedite.write("                     END")
        interMediteLOCCTR = LOCCTR # to assign locations for literals at the end of the program 
        break
    if(line[0]=='.'):
        continue
    label = line[0:10].strip()
    if(len(label) != 0 ):# search and add label
        if(label in symTab):
            errorList.write("duplicated symbol " + label)
        else:
            symTab.update({label : LOCCTR})
            symbolFile.write(label + " "+ LOCCTR[2:]+"\n")
    directive = line[11:20].strip()
    operationCode = directive
    interMediteLOCCTR = LOCCTR
    if(directive =="WORD"):
        LOCCTR = hex(int(LOCCTR, 16) + int("3", 16)) 
    elif(directive == "RESW"):
        operand = int(line[21:39].strip())
        LOCCTR = hex(int(LOCCTR, 16) + (operand*3)) 
    elif(directive== "RESB"):
        operand = int(line[21:39].strip())
        LOCCTR = hex(int(LOCCTR, 16) + (operand))
    elif(directive =="BYTE"):
        if(line[21]=='C'):
            Cvalue = len(line[22:39].strip())-2
            LOCCTR = hex(int(LOCCTR, 16) + (Cvalue))
        elif(line[21]=='X'):
            Xvalue = len(line[22:39].strip())-2
            LOCCTR = hex(int(LOCCTR, 16) + (math.ceil(Xvalue/2)))
    elif(operationCode in optab):
        LOCCTR = hex(int(LOCCTR, 16) + int("3", 16))
    elif(directive !="LTORG"): 
        errorList.write("invalid operation code")
        continue
    if (directive == "LTORG"):
        interMedite.write("          "+line)
    else: 
        interMedite.write(str(interMediteLOCCTR[2:]) +"      "+line)
    if(len(line)>21):#some lines len is less than 21 so an exception will be thrown 
        if(line[21] == "="):
            lit = str(line[22:39].split())
            literals.update({lit[2:-2]:0})     
    if (directive == "LTORG"):
        for i in literals: 
            if (i not in symTab):
                s=str(i)
                symbolFile.write(s + " "+ LOCCTR[2:]+"\n")
                symTab.update({s : LOCCTR})
                interMedite.write(interMediteLOCCTR[2:]+"      *          ="+s+"\n")
                if (i[0] == 'C'):
                    leteralLen  = len(i[2:-1])
                    LOCCTR = hex(int(LOCCTR, 16) + (leteralLen))
                elif(i[0] == 'X'):
                    leteralLen  = len(i[2:-1])
                    LOCCTR = hex(int(LOCCTR, 16) + (math.ceil(leteralLen/2)))
                interMediteLOCCTR = LOCCTR
        literals = {}
if (len(literals)):
    for i in literals: 
        if (i not in symTab):
            s=str(i)
            symbolFile.write(s + " "+ LOCCTR[2:]+"\n")
            symTab.update({s : LOCCTR})
            interMedite.write("\n"+interMediteLOCCTR[2:]+"      *          ="+s+"\n")
            if (i[0] == 'C'):
                leteralLen  = len(i[2:-1])
                LOCCTR = hex(int(LOCCTR, 16) + (leteralLen))
            elif(i[0] == 'X'):
                leteralLen  = len(i[2:-1])
                LOCCTR = hex(int(LOCCTR, 16) + (math.ceil(leteralLen/2)))
            interMediteLOCCTR = LOCCTR
symbolFile.close()

progLen = hex(int(LOCCTR, 16)-int(initialLOCCTR , 16))

readsymTab = open("SymTab.txt", "r")
print("Symbol Table :\n")
while True:
    line = readsymTab.readline()
    if not line:
        break
    print(line)
interMedite.write(LOCCTR[2:])
print("Programe Name = "+progName)
print("Programe length = " + progLen[2:])
print("program location cuonter = " +LOCCTR[2:])
print("Programe start at location = "+initialLOCCTR[2:])