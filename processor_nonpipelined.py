def converttoint(s):#converting the binary string to int
    if s[0]=="1" and len(s)==16:#this handles the case of negative numbers but only for the immediate values.
        strimm=""
        for i in range(len(s)):
            if s[i]=="1":
                strimm+="0"
            else:
                strimm+="1"
        return (converttoint(strimm)+1)*(-1) 
    ans=0
    c=len(s)-1
    for i in range(c+1):
        ans += (2**(c-i))*int(s[i])
    return ans
def Ifetch(l,i):#fetching the instruction from the instructino memory
    return l[i]
def Idecode(s):#decoding the instruction on the basis of i format  r format j format
    if s[0:6]=="000000" or s[0:6]=="011100": # R format isntructions and MUL instruction being decoded
        rs = converttoint(s[6:11])
        rt = converttoint(s[11:16])
        rd = converttoint(s[16:21])
        func  = s[26:32]
        return [rs,rt,rd,func]
    elif s[0:6]!="000010" and s[0:6]!="000011": # I format instructions being decoded.
        rs = converttoint(s[6:11])
        rt = converttoint(s[11:16])
        immediate = converttoint(s[16:32])
        return [rs,rt,immediate]
    else: # j format isntructions being decoded.
        return [converttoint(s[6:32])]

def AluExec(func,a,b,opcode): #performing the mathematical opeerations dependiong upon the func/opcode as required
    if func=="100000" or opcode=="100011" or opcode=="101011" or opcode=="001000":#add for the load add addi,store.
        return a+b
    elif func=="100010":#sub
        return a-b 
    elif opcode=="000100": #equality comparison for beq
        return a==b
    elif opcode=="011100": #mul 
        return a*b
    
def MemAccess(datamem,x):#accessing the memory 
    return datamem[x]
def WriteBack(regmem,idx,alu_val):#performing the Write back operations
    regmem[idx]=alu_val
    return regmem


instruction_memory = [] #reading and storing the instructions in Instruction memory
data_memory = [0]*1024 #total 1024 memory locations
reg_memory  = { #the register memory where all the registers are assinged values 0 as the mips assembler does
    0: 0,   # $zero
    1: 0,   # $at
    2: 0,   # $v0
    3: 0,   # $v1
    4: 0,   # $a0
    5: 0,   # $a1
    6: 0,   # $a2
    7: 0,   # $a3
    8: 0,   # $t0
    9: 0,   # $t1
    10: 0,  # $t2
    11: 0,  # $t3
    12: 0,  # $t4
    13: 0,  # $t5
    14: 0,  # $t6
    15: 0,  # $t7
    16: 0,  # $s0
    17: 0,  # $s1
    18: 0,  # $s2
    19: 0,  # $s3
    20: 0,  # $s4
    21: 0,  # $s5
    22: 0,  # $s6
    23: 0,  # $s7
    24: 0,  # $t8
    25: 0,  # $t9
    26: 0,  # $k0
    27: 0,  # $k1
    28: 0,  # $gp
    29: 0,  # $sp
    30: 0,  # $fp
    31: 0   # $ra
}

f = open('instructions for factorial','r') #reading the instructions from the respective files that contain machine code.
# f = open('instructions for fibonacci','r')
temp = f.readlines()
instruction_memory = [i.strip() for i in temp] #cleaning the instructions.
clock_cycles=0
i=0
while i < len(instruction_memory): #looping over the instructions and executing them one by one
    alu_val=0
    flag=False #for checking the beq instruction
    current_instruction = Ifetch(instruction_memory,i)#instructions fetch complete
    l = Idecode(current_instruction)#instructions decoded
    #performing the alu operations.
    if len(l)==4: # This indicates the R format instruction was decoded as it contains 4 fields rs,rt,rd,func
        alu_val = AluExec(l[3],reg_memory[l[0]],reg_memory[l[1]],current_instruction[0:6])
    elif len(l)==3: #this indicates 
        
        if current_instruction[0:6]=="100011"or current_instruction[0:6]=="001000" : #load and addi execution.
            alu_val=AluExec("000000",reg_memory[l[0]],l[2],current_instruction[0:6])
        elif current_instruction[0:6]=="101011":#sw execution
            alu_val =AluExec("000000",reg_memory[l[0]],l[2],current_instruction[0:6])
        else:
            flag = AluExec("000000",reg_memory[l[0]],reg_memory[l[1]],current_instruction[0:6])
    
    #taking the branch decisions
    
    if flag==True:
        i+=l[2]+1
        clock_cycles+=1
        continue
    if i>len(instruction_memory):
        break

    # performing the memory access if required
    temporary_var_mem=0
    if current_instruction[0:6]=="100011" : #if the instruction is a load word instruction
        temporary_var_mem=data_memory[alu_val]
    elif current_instruction[0:6]=="101011": #if the instruction is a store word instruction.
        # print(alu_val)
        data_memory[alu_val]=reg_memory[l[1]]
        # print(f"this is {alu_val} and this is reg val {reg_memory[l[1]]} and this is the instruction no {i}")

    #performing the memory writeback if required. 
    if current_instruction[0:6]=="000000" or current_instruction[0:6]=="011100":#write back for the rformat instructions and mul
        # reg_memory[l[2]]=alu_val
        reg_memory = WriteBack(reg_memory,l[2],alu_val)
    elif current_instruction[0:6]=="001000": #for addi
        # reg_memory[l[1]]=alu_val
        reg_memory = WriteBack(reg_memory,l[1],alu_val)

    # print(i)
    i+=1
    clock_cycles+=1


print(f"the factorial is {reg_memory[11]}")  
# print(*data_memory[0:8])
print(f"the no of clock cycles taken by the program is {clock_cycles}")


