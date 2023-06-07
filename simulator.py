memory = [0] *256

def initialize_memory():
    memory = [0] * 256 

    binary_data = input().strip().split()
    for i, data in enumerate(binary_data):
        memory[i] = int(data, 2)
    return memory

def fetch_instruction(memory, pc):
    return memory[pc]

def execute_instruction(instruction, registers):
    opcode = instruction >> 11

    if opcode == 0b00000:  # Addition
        reg1 = (instruction >> 8) & 0b111
        reg2 = (instruction >> 5) & 0b111
        reg3 = instruction & 0b111
        result = registers[reg2] + registers[reg3]
        if result > 0xFFFF:  # Overflow occurred
            registers[reg1] = 0
            registers[6] = 1  # Set overflow flag
        else:
            registers[reg1] = result

    elif opcode == 0b00001:  # Subtraction
        reg1 = (instruction >> 8) & 0b111
        reg2 = (instruction >> 5) & 0b111
        reg3 = instruction & 0b111
        result = registers[reg2] - registers[reg3]
        if result < 0:  # Overflow occurred
            registers[reg1] = 0
            registers[6] = 1  # Set overflow flag
        else:
            registers[reg1] = result

    elif opcode == 0b00010:  # Move Immediate
        reg1 = (instruction >> 8) & 0b111
        immediate = instruction & 0b1111111
        registers[reg1] = immediate

    elif opcode == 0b00011:  # Move Register
        reg1 = (instruction >> 8) & 0b111
        reg2 = instruction & 0b111
        registers[reg1] = registers[reg2]

    elif opcode == 0b00100:  # Load
        reg1 = (instruction >> 8) & 0b111
        memory_address = instruction & 0b1111111
        registers[reg1] = memory[memory_address]

    elif opcode == 0b00101:  # Store
        reg1 = (instruction >> 8) & 0b111
        memory_address = instruction & 0b1111111
        memory[memory_address] = registers[reg1]

    elif opcode == 0b00110:  # Multiply
        reg1 = (instruction >> 8) & 0b111
        reg2 = (instruction >> 5) & 0b111
        reg3 = instruction & 0b111
        result = registers[reg2] * registers[reg3]
        if result > 0xFFFF:  # Overflow occurred
            registers[reg1] = 0
            registers[6] = 1  # Set overflow flag
        else:
            registers[reg1] = result

    elif opcode == 0b00111:  # Divide
        reg3 = (instruction >> 8) & 0b111
        reg4 = instruction & 0b111
        if registers[reg4] == 0:  # Check for division by zero
            registers[0] = 0
            registers[1] = 0
            registers[6] = 1  # Set overflow flag
        else:
            registers[0] = registers[reg3] // registers[reg4]
            registers[1] = registers[reg3] % registers[reg4]

    elif opcode == 0b01000:  # Right Shift
        reg1 = (instruction >> 8) & 0b111
        shift_amount = instruction & 0b1111111
        registers[reg1] >>= shift_amount

    elif opcode == 0b01001:  # Left Shift
        reg1 = (instruction >> 8) & 0b111
        shift_amount = instruction & 0b1111111
        registers[reg1] <<= shift_amount

    elif opcode == 0b01010:  # Exclusive OR
        reg1 = (instruction >> 8) & 0b111
        reg2 = (instruction >> 5) & 0b111
        reg3 = instruction & 0b111
        registers[reg1] = registers[reg2] ^ registers[reg3]

    elif opcode == 0b01011:  # OR
        reg1 = (instruction >> 8) & 0b111
        reg2 = (instruction >> 5) & 0b111
        reg3 = instruction & 0b111
        registers[reg1] = registers[reg2] | registers[reg3]

    elif opcode == 0b01100:  # AND
        reg1 = (instruction >> 8) & 0b111
        reg2 = (instruction >> 5) & 0b111
        reg3 = instruction & 0b111
        registers[reg1] = registers[reg2] & registers[reg3]

    elif opcode == 0b01101:  # Invert
        reg1 = (instruction >> 8) & 0b111
        reg2 = instruction & 0b111
        registers[reg1] = ~registers[reg2] & 0xFFFF

    elif opcode == 0b01110:  # Compare
        reg1 = (instruction >> 8) & 0b111
        reg2 = instruction & 0b111
        if registers[reg1] < registers[reg2]:
            registers[6] = 1  # Set less than flag
        elif registers[reg1] > registers[reg2]:
            registers[6] = 0  # Clear less than flag
        else:
            registers[6] = 1  # Set equal flag

    elif opcode == 0b01111:  # Unconditional Jump
        mem_addr = instruction & 0b1111111
        return False, mem_addr

    elif opcode == 0b11100:  # Jump If Less Than
        mem_addr = instruction & 0b1111111
        if registers[6] == 1:  # Less than flag is set
            return False, mem_addr

    elif opcode == 0b11101:  # Jump If Greater Than
        mem_addr = instruction & 0b1111111
        if registers[6] == 0:  # Greater than flag is set
            return False, mem_addr

    elif opcode == 0b11111:  # Jump If Equal
        mem_addr = instruction & 0b1111111
        if registers[6] == 1:  # Equal flag is set
            return False, mem_addr

    elif opcode == 0b11010:  # Halt
        return True, 0

    return False, registers[7] + 1  # PC register

def execute_instructions_from_file(filename):
    
    registers = [0] * 8

    with open(filename, 'r') as file:
        instructions = file.readlines()

    halted = False
    pc = 0

    while not halted and pc < len(instructions):
        current_pc = registers[7]
        instruction = int(instructions[pc], 2)
        halted, new_pc = execute_instruction(instruction, registers)
        # Print PC and RF state
        print(f'{current_pc:07b}', end=' ')
        for i in range(7):
            print(f'{registers[i]:016b}', end=' ')
        print(f'{registers[6]:016b}')  # FLAGS register

        registers[7] = new_pc  # Update PC register

    # Print complete memory dump
    #for data in memory:
        #print(f'{data:016b}')


    print("Execution halted.")    


# def simulate():
#     memory = initialize_memory()
#     registers = [0] * 8  # R0-R6, FLAGS, PC

#     halted = False
#     while not halted:
#         current_pc = registers[7]  # PC register
#         instruction = fetch_instruction(memory, current_pc)
#         halted, new_pc = execute_instruction(instruction, registers)
        

#         # Print PC and RF state
#         print(f'{current_pc:07b}', end=' ')
#         for i in range(7):
#             print(f'{registers[i]:016b}', end=' ')
#         print(f'{registers[6]:016b}')  # FLAGS register

#         registers[7] = new_pc  # Update PC register

    # Print complete memory dump
    #for data in memory:
        #print(f'{data:016b}')

execute_instructions_from_file("")