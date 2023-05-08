def opcodes(mnemonic):                        # mov not included
    if mnemonic == "add":
        return '00000'
    if mnemonic == "sub":
        return '00001'
    if mnemonic == "ld":
        return "00100"
    if mnemonic == "st":
        return "00101"
    if mnemonic == "mul":
        return "00110"
    if mnemonic == "div":
        return "00111"
    if mnemonic == "rs":
        return "01000"                           
    if mnemonic == "ls":
        return "01001"
    if mnemonic == "xor":
        return "01010"
    if mnemonic == "or":
        return "01011"
    if mnemonic == "and":
        return "0100"
    if mnemonic == "not":
        return "01101"
    if mnemonic == "cmp":
        return "01110"
    if mnemonic == "jmp":
        return "01111"
    if mnemonic == "jlt":
        return "11100"
    if mnemonic == "jgt":
        return "11101"
    if mnemonic == "je":
        return "11111"
    if mnemonic == "hlt":
        return "11010"                                        
    else:
        return mnemonic






def registercodes(reg):
    if reg == "R0":
        return "000"
    if reg == "R1":
        return "001"
    if reg == "R2":
        return "010"
    if reg == "R3":
        return "011"
    if reg == "R4":
        return "100"
    if reg == "R5":
        return "101"
    if reg == "R6":
        return "110"  
    else:
        return reg       

def immediate(number):
    if number.startswith("$"):
        number = number[1:]
        number = int(number)
        if int(number)<=127 and int(number)>=0:
            number = str(bin(number))[2:]
            if len(number)<7:
                size = len(number)
                number = ("0"*(7-size))+number
                return number
        else:
            return "immediate error"    
    else:
        return number


#def variableskakyakarun(lst[]):
    # if lst[0] == "var":
    #     varaddress = bin(0000000)




flags = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #12 unused bits # index 12-overflow flag
                                                                  # index 13- less than flag
                                                                  # index 14- greater than flag
                                                                  # index 15- equal flag

#labels ke liye label-line number dictionary

label_dict = {}
var_dict = {}
line_number_dict = {}

lines = []
f = open('textinput.txt', 'r')
while True :
    line = f.readline()
    if line.startswith("var"):
        var_dict[line[4:-1]] = ""                   # variable ka name var dict main abhi empty string ke sath jpd diya hia.
        continue
    if not line : 
        break
    lines.append(line.strip())
f.close()   

#print(var_dict)
#print(lines)



# PASS 1 ////////////        main mnemonics, registers, line addresses and removal of labels   

varaddress = bin(0000000)

for i in range(len(lines)):
    if ":" in lines[i]:
        label_dict[lines[i]] = i                 # i is the number of line at whichh label occurs starting from 0.
        lines[i] = lines[i][lines[i].find(":")+1:]        # empty list in place of label. 
    
    binaryofline = str(bin(i))[2:]
    
    lengthofaddress = len(binaryofline)

    if lengthofaddress<7:
        binaryofline = ("0"*(7-lengthofaddress))+binaryofline             #line addresses with lines in a dict

    line_number_dict[binaryofline] = lines[i]   

      
    #print(lines)

    lines[i] = lines[i].split()
    


    for j in range((len(lines[i]))-1,-1,-1):
        try :
            if lines[i][j] == "mov":
                if len(lines[i][j+2]) == 7:
                    lines[i][j] = "00010"
                if len(lines[i][j+2]) == 3:
                    lines[i][j] = "00011"    
            lines[i][j] = opcodes(lines[i][j])
            lines[i][j] = registercodes(lines[i][j])
            lines[i][j] = immediate(lines[i][j])
            


        except: 
            pass    

        
            
            





print(lines)
# #print(binary)
# print(label_dict) 
# print(line_number_dict)  





