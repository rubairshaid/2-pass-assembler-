interMedite = open("INTMD.mdt" , "r")
listingFile = open("listing.lst","w")
objectFile = open("objectF.obj","w")
opcode = open("OPTAB.txt")
symbolFile = open("SymTab.txt" , "r") 
ErrorPass2 = open("pass2Error","w")
optab = {}
symTab = {}

while True:
    line = opcode.readline()
    if not line:
        break
    op = line[0:11].strip()
    opnum = line[11:13].strip()
    optab.update({op : opnum})

while True:
    line = symbolFile.readline()
    if not line:
        break
    sym = line.split()
    symTab.update({sym[0] : sym[1]})

line = interMedite.readline()

if (line[21:30].strip() == "START"):
    progName = line[10:20].strip()
    startAdd = line[0:4]
    listingFile.write(line)
    line = interMedite.readline()


INTMDTLINES= interMedite.readlines() #reading the whole lines 
proLEN = INTMDTLINES[-1] #setting the program length
objectFile.write("H^"+progName + ' '*(6-len(progName)) + "^00" + startAdd + "^00" +proLEN )

#initialize first text record 
textRString ="\nT^00"+startAdd+"^^"
interMedite.close()
interMedite = open("INTMD.mdt" , "r")
line = interMedite.readline()
textRCounter = 0 
while (True):
    line = interMedite.readline()
    if not line:
        break
    if (line[21:30].strip() == "END"):
        listingFile.write(line)
        continue
    operationCode = line [21:30].strip() 
    if(operationCode in optab):
        symbol = line [31:49].strip() # symbol is the operand 
        if(len(symbol)!=0):
            indexed = False 
            if(",X" in symbol):
                symbol = symbol[:-2]
                indexed = True
            if("=" in symbol):
                symbol = symbol[1:]
            if(symbol in symTab):
                lineObjectCode = optab[operationCode] #get the opcode
                if (indexed):
                    operandAdd = hex(int(symTab[symbol], 16) + int("8000", 16))
                    lineObjectCode += operandAdd[2:]##
                else:
                    lineObjectCode += symTab[symbol]##
            else:
                lineObjectCode = optab[operationCode]
                lineObjectCode +="0000"
                ErrorPass2.write("undefined symbol")
        else:
            lineObjectCode = optab[operationCode]
            lineObjectCode +="0000"##
        listingFile.write(line[0:-1] + "     " + lineObjectCode+"\n")
        if(textRCounter+3<=30):
            textRCounter+=3
            textRString+= lineObjectCode+"^"
        else:
            hexaTextRCounter = hex(textRCounter)
            textRString = textRString[:10]+hexaTextRCounter[2:]+"^"+textRString[11:]
            objectFile.write(textRString)
            textRCounter=3
            textRString ="\nT^00"+line[0:4]+"^^"+lineObjectCode+"^"
    elif(operationCode=="WORD"):
        wordValue = int(line[31:49].strip())
        hexaValue = hex(wordValue)[2:]
        lineObjectCode = "0"*(6-len(hexaValue)) + hexaValue
        listingFile.write(line[0:-1] + "     " + lineObjectCode+"\n")
        if(textRCounter+3<=30):
            textRCounter+=3
            textRString+= lineObjectCode+"^"
        else:
            hexaTextRCounter = hex(textRCounter)
            textRString = textRString[:10]+hexaTextRCounter[2:]+"^"+textRString[11:]
            objectFile.write(textRString)
            textRCounter=3
            textRString ="\nT^00"+line[0:4]+"^^"+lineObjectCode+"^"
    elif(operationCode=="BYTE"):
        charValue = line[33:48].strip()
        charValue = charValue[:-1]
        print (charValue)
        if(line[31]=='C'):
            lineObjectCode=""
            for i in charValue:
                lineObjectCode += format(ord(i), "x")
            byteCounter = len(charValue)
        elif(line[31]=="X"):
            lineObjectCode = charValue
            byteCounter = int(len(charValue)/2)
        listingFile.write(line[0:-1] + "     " + lineObjectCode+"\n")

        if(textRCounter+byteCounter<=30):
            textRCounter+=byteCounter
            textRString+= lineObjectCode+"^"
        else:
            hexaTextRCounter = hex(textRCounter)
            textRString = textRString[:10]+hexaTextRCounter[2:]+"^"+textRString[11:]
            objectFile.write(textRString)
            textRCounter=byteCounter
            textRString ="\nT^00"+line[0:4]+"^^"+lineObjectCode+"^"

    elif (operationCode == "RESW" or operationCode== "RESB"):
        operand = int(line[31:49].strip())
        if(line[24]=="W"):
            adressAfterRes = hex(int(line[0:4], 16) + (operand*3))[2:]
        else:
            adressAfterRes = hex(int(line[0:4], 16) + (operand))[2:]
        listingFile.write(line)
        if(textRCounter!=0):
            hexaTextRCounter = hex(textRCounter)
            textRString = textRString[:10]+hexaTextRCounter[2:]+"^"+textRString[11:]
            objectFile.write(textRString)
            textRCounter=0
        textRString ="\nT^00"+adressAfterRes+"^^"
    elif(operationCode=="LTORG"):
        listingFile.write(line)
    elif(len(operationCode)>0 and operationCode[0] == '='):
        charValue = line[24:30].strip()
        charValue = charValue[:-1]
        if(line[22]=='C'):
            lineObjectCode=""
            for i in charValue:
                lineObjectCode += format(ord(i), "x")
        elif(line[22]=="X"):
            lineObjectCode = charValue
        listingFile.write(line[0:-1] + "     " + lineObjectCode+"\n")
        if(textRCounter+(len(lineObjectCode)/2) <=30):
            textRCounter+=int(len(lineObjectCode)/2)
            textRString+= lineObjectCode+"^"
        else:
            hexaTextRCounter = hex(textRCounter)
            textRString = textRString[:10]+hexaTextRCounter[2:]+"^"+textRString[11:]
            objectFile.write(textRString)
            textRCounter=int(len(lineObjectCode)/2)
            textRString ="\nT^00"+line[0:4]+"^^"+lineObjectCode+"^"

hexaTextRCounter = hex(textRCounter)
textRString = textRString[:10]+hexaTextRCounter[2:]+"^"+textRString[11:]
objectFile.write(textRString)
objectFile.write("\nE^00"+startAdd)


