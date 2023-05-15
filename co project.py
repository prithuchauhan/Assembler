import re


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
    if reg == "FLAGS":
        return "111"    
    else:
        return reg    



def contains_non_binary(string):
    pattern = re.compile('[^01]')
    return bool(pattern.search(string))
           

def immediate(number):
    if number.startswith("$"):
        number = number[1:]
        number = int(number)
        if int(number)<=127 and int(number)>=0:                     # 127 error
            number = str(bin(number))[2:]
            if len(number)<=7:
                size = len(number)
                number = ("0"*(7-size))+number
                return number
        else:
            return "immediateerror"    
    else:
        return number


#def variableskakyakarun(lst[]):
    # if lst[0] == "var":
    #     varaddress = bin(0000000)




FLAGS = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #12 unused bits # index 12-overflow flag
                                                                  # index 13- less than flag
                                                                  # index 14- greater than flag
                                                                  # index 15- equal flag

#labels ke liye label-line number dictionary

label_dict = {}
var_dict = {}
line_number_dict = {}
linelistwithvar = []
error = False

lines = []
f = open('hardgen4.txt', 'r')
while True :
    line = f.readline()
    linelistwithvar.append(line.strip())
    if line.startswith("var"):
        var_dict[line[4:-1]] = ""                   # variable ka name var dict main abhi empty string ke sath jpd diya hia.
        continue
    if not line : 
        break
    lines.append(line.strip())
f.close()   

#print(var_dict)
#print(lines)
lineswithoutlabels = []
var_beginning = True
#print(linelistwithvar)

for i in range(len(linelistwithvar)):
    if linelistwithvar[i].startswith('var'):
        if i>0 and not linelistwithvar[i-1].startswith('var'):
            print("All variables not defined in the beginning")
            var_beginning = False
            break
            


# PASS 1 ////////////        main mnemonics, registers, line addresses and removal of labels   
if error == False:
    varaddress = bin(0000000)

    for i in range(len(lines)):

        

        if ":" in lines[i]:
            position = lines[i].rfind(":")
            label_dict[lines[i][:position]] = i                # i is the number of line at which label occurs starting from 0.
        
            newline =  lines[i][position+2:]
            lineswithoutlabels.append(newline)
        
        else:
            lineswithoutlabels.append(lines[i])      # bina label ke sab ismain aa gayi.  
            
    #print(lineswithoutlabels)
    #print(label_dict)

    #print(label_dict)
    #print(lineswithoutlabels)   

    for i in range(len(lineswithoutlabels)):

        
        binaryofline = str(bin(i))[2:]
        
        lengthofaddress = len(binaryofline)

        if lengthofaddress<=7:
            binaryofline = ("0"*(7-lengthofaddress))+binaryofline             # line addresses with lines in a dict

        line_number_dict[binaryofline] = lineswithoutlabels[i]    

        
        #print(lines)
        if isinstance(lineswithoutlabels[i],str) == True:
            lineswithoutlabels[i] = lineswithoutlabels[i].split()
            #print(lineswithoutlabels[i])
        


        for j in range((len(lineswithoutlabels[i])-1),-1,-1):
            try :
                if lineswithoutlabels[i][j] == "mov":                                  # mov ka chakkar khtm.
                    if len(lineswithoutlabels[i][j+2]) == 7:
                        lineswithoutlabels[i][j] = "00010" 
                    if len(lineswithoutlabels[i][j+2]) == 3:
                        lineswithoutlabels[i][j] = "00011"        
                lineswithoutlabels[i][j] = opcodes(lineswithoutlabels[i][j])
                lineswithoutlabels[i][j] = registercodes(lineswithoutlabels[i][j])
                lineswithoutlabels[i][j] = immediate(lineswithoutlabels[i][j])
                


            except: 
                pass    


    #print(line_number_dict)
    #print(lineswithoutlabels)

    line_numbers = len(line_number_dict)

    for i in var_dict:     
        var_dict[i] = str(bin(line_numbers))[2:]
        line_numbers += 1
        
    #print(var_dict)  

    for i in var_dict:
        
        if len(var_dict[i])<7:
            var_dict[i] = "0"*(7-(len(var_dict[i])))+var_dict[i]

    #print(var_dict)

    newlabeldict = {}

    for i in label_dict:
        j = i[:-1]
        newlabeldict[j] = label_dict[i]                # ab zaroorat nahi padegi

        
        
    for i in label_dict:
        label_line = str(bin(label_dict[i]))[2:] 
        if len(label_line)<7:
            label_line = "0"*(7-len(label_line))+label_line
        label_dict[i] = label_line        

    #print(label_dict)
    #print(var_dict)        

    # 2nd Pass                                   # variables replaced with line codes. # labels replaced with line codes

    for i in range(len(lineswithoutlabels)):
        for j in range((len(lineswithoutlabels[i]))-1,-1,-1):
            try:
                if lineswithoutlabels[i][j] in var_dict:                      
                    lineswithoutlabels[i][j] = var_dict[lineswithoutlabels[i][j]]
                if lineswithoutlabels[i][j] in label_dict:
                    lineswithoutlabels[i][j] = label_dict[lineswithoutlabels[i][j]]
            except:
                pass

    # labels replaced by where they are defined



    #print(var_dict)

    #print(label_dict)
    #print(var_dict.values())

    #print(lineswithoutlabels)     


    # 3 pass error hatao and saare instructions ko 16 bits main likho.
    joinedlineslist = []
    error = False
    immediate_error = False
    varinplaceoflabel = False
    labelinplaceofvar = False
    nohltpresent = False
    hltnotlastinstruction = False
    hlt_present = False
    registernamewrong = False
    typoininstructionname = False
    undefinedlabel = False
    undefinedvariable = False
    nonbinary = False

    
    
    for i in range(len(lineswithoutlabels)):
        for j in range((len(lineswithoutlabels[i]))):
            if lineswithoutlabels[i][j] == '11010':
                hlt_present = True
                break

    for i in range(len(lineswithoutlabels)):
        for j in range((len(lineswithoutlabels[i]))):


            if lineswithoutlabels[i][j] == '111':
                if lineswithoutlabels[i][j-2] == '00011':
                    illegalflag = False
                else:
                    if var_beginning == True:
                        print("illegal use of FLAGS register at line " + str(i+1+len(var_dict)))
                        error =True
                    else:
                        print("illegal use of flag register")
                        illegalflag = True
                        error = True
                    break
            

            if lineswithoutlabels[i][j] == None:
                if var_beginning == True:
                    print("general syntax error at line "+ str(i+1+len(var_dict)))
                    error =True
                else:
                    print("general syntax error")
                    error = True
                break



            
            if lineswithoutlabels[i][j] == "immediateerror":                   # saare error yahan aynge.
                if var_beginning == True:
                    print("Immediate Value out of bounds at line "+ str(i+1+len(var_dict)))
                    error= True
                else:
                    print("immediate value out of bounds")
                    immediate_error = True
                    error = True
                break
                
                    
            
            # variable in place of label    jump vale saare instructions
            
            if lineswithoutlabels[i][j] == '01111' or lineswithoutlabels[i][j] =='11100' or lineswithoutlabels[i][j] =='11101' or lineswithoutlabels[i][j] =='11111':    
                if lineswithoutlabels[i][j+1] in var_dict:
                    if var_beginning == True:
                        print("variable in place of label at line "+ str(i+1+len(var_dict)))
                        error = True
                    else:
                        print("variable in place of label")
                        varinplaceoflabel = True
                        error = True
                    break
                    
                  
            
            
            #label in place of variable  
               
            if lineswithoutlabels[i][j] == '00100' or lineswithoutlabels[i][j] == '00101':
                if lineswithoutlabels[i][j+2] in label_dict:
                    if var_beginning == True:
                        print("label in place of variable at line " + str(i+1+len(var_dict)))
                        error =True
                    else:
                        print("label in place of variable")
                        labelinplaceofvar = True
                        error =True
                    break
                    
                        
            
            #hlt instructions error
            
                

            #typos in instruction name
           
            if len(lineswithoutlabels[i][j]) == 2:
                if (lineswithoutlabels[i][j][0] == 'R') or lineswithoutlabels[i][j][0] == 'r' or lineswithoutlabels[i][j].startswith("reg"):
                    if var_beginning == True:
                        print("not a valid register at line "+ str(i+1+len(var_dict)))
                        error = True
                    else:
                        print("not a valid register name")
                        registernamewrong = True
                        error = True
                        break

            
                

            
            if lineswithoutlabels[i][j] == '01111' or lineswithoutlabels[i][j] =='11100' or lineswithoutlabels[i][j] =='11101' or lineswithoutlabels[i][j] =='11111':
                if lineswithoutlabels[i][j+1] not in label_dict.values():
                    if var_beginning == True:
                        print("undefined label name at line " + str(i+1+len(var_dict)))
                        error = True
                    else:
                        print("undefined label name")
                        undefinedlabel = True
                        error = True
                    break
                        

            if lineswithoutlabels[i][j] == '00100' or lineswithoutlabels[i][j] == '00101':
                if lineswithoutlabels[i][j+2] not in var_dict.values():
                    if var_beginning == True:
                        print("undefined variable at line" + str(i+1+len(var_dict)))
                        error = True
                    else:
                        print("undefined variable")
                        undefinedvariable = True
                        error = True
                    break

                                         
            if (contains_non_binary(lineswithoutlabels[i][j])) == True:
                
                if var_beginning == True:
                    print("general syntax error at line " + str(i+1+len(var_dict)))
                    error = True
                    nonbinary = True
                else:
                    print("general syntax error")
                    error = True     
                    nonbinary = True               
                break
            
            if lineswithoutlabels[i][0] == '00000' or lineswithoutlabels[i][0] == '00001' or lineswithoutlabels[i][0] == '00110' or lineswithoutlabels[i][0] == '01010' or lineswithoutlabels[i][0] == '01011' or lineswithoutlabels[i][0] == '01100':
                if var_beginning == True:
                    if len(lineswithoutlabels[i]) != 4:
                        print("wrong number of operands in command at line " + str(i+1+len(var_dict)))
                        error = True
                else:
                    if len(lineswithoutlabels[i]) != 4:
                        print("wrong number of operands")
                        error = True
                break
            if lineswithoutlabels[i][0] == '00111' or lineswithoutlabels[i][0] == '01101' or lineswithoutlabels[i][0] == '01110':
                if var_beginning == True:
                    if len(lineswithoutlabels[i]) != 3:
                        print("wrong number of operands at line " + str(i+1+len(var_dict)))
                        error = True
                else:
                    if len(lineswithoutlabels[i]) != 3:
                        print("wrong number of operands")
                        error = True
                break            

    
    if hlt_present == False:
        print("no hlt instruction present")
        error = True
    if hlt_present == True:
        lastline = len(lineswithoutlabels)
        lastline = lastline-1
        if (lineswithoutlabels[lastline][0] != '11010'):
            print("hlt not last instruction")
            hltnotlastinstruction = True
            error =True


    
    
    

    if var_beginning == True:
        if error == False:
            for i in range(len(lineswithoutlabels)):
                finallines = "".join(lineswithoutlabels[i]) 
                joinedlineslist.append(finallines)

    finallist = []

    for i in joinedlineslist:
        if len(i)<16:
            j = i[0:5]+("0"*(16-len(i)))+i[5:]
            finallist.append(j)
        else:
            finallist.append(i)

    for i in finallist:
        print(i)






                
                





    #for i in range(len(lines)):
    #   print("".join(lines[i][:]))
    # #print(binary)
    #print(label_dict) 







