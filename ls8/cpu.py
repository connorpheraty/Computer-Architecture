import sys

"""CPU functionality."""

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8

        self.instructions = {}

        self.address = 0
        self.SP = 0

    def init_SP(self):
        self.SP = 0
        
    def add_instructions(self):
        
        self.instructions['LDI'] = 0b10000010
        self.instructions['PRN'] = 0b01000111
        self.instructions['HLT'] = 0b00000001
        self.instructions['MUL'] = 0b10100010
        self.instructions['PUSH'] = 0b01000101
        self.instructions['POP'] = 0b01000110
        
    def ram_read(self):
        print(self.ram)

    def ram_write(self, value):
        self.ram[self.address] = value
        self.address +=1

    def load(self):
        """Load a program into memory."""
        
        progname = sys.argv[1]
        
        with open(progname) as f:
            for line in f:
                line = line.split('#')[0]
                line = line.strip() # Lose whitespace
                
                if line == '':
                    continue
                
                val = int(line, base=2)
                
                self.ram[self.address] = val
                self.address +=1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        
        else:
            raise Exception("Unsupported ALU operation")


    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""       
        halted = False 
        pc = 0
        self.init_SP()

        
        print('Running program...')
        while not halted:
            instruction = self.ram[pc]
            
            if instruction == self.instructions['LDI']:
                reg_num = self.ram[pc+1]
                value = self.ram[pc+2]
                
                self.reg[reg_num] = value
                
                pc += 3

            if instruction == self.instructions['PUSH']:
                self.reg[self.SP] -=1  # Decrement the stack pointer
                reg_num = self.ram[pc+1]
                reg_val = self.reg[reg_num]

                self.ram[self.reg[self.SP]] = reg_val # Copy reg value into memory at address SP

                pc +=2

            if instruction == self.instructions['POP']:
                val = self.ram[self.reg[self.SP]]
                reg_num = self.ram[pc + 1]
                self.reg[reg_num] = val # Copy val from memory at SP into register

                self.reg[self.SP] += 1 # Increment SP

                pc += 2
                
            if instruction == self.instructions['PRN']:
                reg_num = self.ram[pc+1]
                print(self.reg[reg_num])
                
                pc += 2

            if instruction == self.instructions['MUL']:
                reg_num1 = self.reg[self.ram[pc+1]]
                reg_num2 = self.reg[self.ram[pc+2]]

                self.reg[self.ram[pc+1]] = reg_num1 * reg_num2

                pc += 3
                
            if instruction == self.instructions['HLT']:
                halted= True
                pc+=1
