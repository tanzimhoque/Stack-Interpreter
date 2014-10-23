import os
import sys

from rpython.rlib import jit

INSTR_ADD = 0
INSTR_SUB = 1
INSTR_PRINT = 2
INSTR_JUMP = 3
INSTR_INT = 4
INSTR_JNZERO = 5
INSTR_LOAD = 6
INSTR_STORE = 7
INSTR_POP = 8


jitdriver = jit.JitDriver(greens=['pc', 'program'], reds=['stack', 'memory'])

def execute(program, stack, memory):
	pc = 0
	while pc < len(program):
		jitdriver.can_enter_jit(pc=pc, program=program, stack=stack, memory=memory)
		jitdriver.jit_merge_point(pc=pc, program=program, stack=stack, memory=memory)
    	#ADD=0, SUB=1, PRINT=2, JUMP=3, INT=4, JNZERO = 5, LOAD = 6, STORE = 7
		line = program[pc]
		
		if line == INSTR_ADD:
			result = (stack.pop() + stack.pop())
			stack.push(result)
			pc += 2
		elif line == INSTR_SUB:
			result = stack.pop() - program[pc + 1]
			stack.push(result)
			pc += 2
		elif line == INSTR_PRINT:
			output = stack.pop()
			print output
			pc += 2
		elif line == INSTR_JUMP:
			pc = (program[pc + 1] * 2)
		elif line == INSTR_INT:
			stack.push(program[pc + 1])
			pc += 2
		elif line == INSTR_JNZERO:
			if stack.stack[stack.pointer - 1] > 0:
				pc = (program[pc + 1] * 2)
			else:
				pc += 2
		elif line == INSTR_LOAD:
			output = memory.load(program[pc + 1])
			stack.push(output)
			pc += 2
		elif line == INSTR_STORE:
			memory.store(program[pc + 1], stack.stack[stack.pointer - 1])
			pc += 2
		elif line == INSTR_POP:
			stack.pop()
			pc += 2


class Memory(object):
	def __init__(self, memory_limit):
		self.stack = [0] * memory_limit
		self.pointer = 0
	def load(self, loc):
		return self.stack[loc]
		
	def store(self, loc, val):	
		self.stack[loc] = val
		self.pointer += 1

class Stack(object):
	def __init__(self, stack_limit):
		self.stack = [0] * stack_limit
		self.pointer = 0;
	
	def pop(self):
		self.pointer -= 1
		return self.stack[self.pointer]
	
	def push(self, input):
		self.stack[self.pointer] = input
		self.pointer += 1

def run(fp):
    program_content = ""
    p = []
    while True:
    
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_content += read

	p = program_content.splitlines()
	
    os.close(fp)
    program_interpreter(p)
    
def program_interpreter(p):
	stack_limit = 0
	memory_limit = 0
	
	max_stack_limit = 0
	max_memory_limit = 0
	
	program = []
	
	counter = 0
    
	while counter < len(p):
   		line = p[counter]
		if line[:3] == "ADD":
			stack_limit -= 1
			program.append(INSTR_ADD)
			program.append(0)			
		elif line[:3] == "INT":
			stack_limit += 1
			program.append(INSTR_INT)
			program.append(int(line.strip("INT ")))
		elif line[:4] == "JUMP":
			program.append(INSTR_JUMP)
			program.append(int(line.strip("JUMP ")))
		elif line[:3] == "SUB":
			program.append(INSTR_SUB)
			program.append(int(line.strip("SUB ")))
		elif line[:6] == "JNZERO":
			program.append(INSTR_JNZERO)
			program.append(int(line.strip("JNZERO ")))
		elif line[:5] == "PRINT":
			program.append(INSTR_PRINT)
			program.append(0)
		elif line[:4] == "LOAD":
			stack_limit += 1
			memory_limit -= 1
			program.append(INSTR_LOAD)
			program.append(int(line.strip("LOAD ")))
		elif line[:5] == "STORE":
			memory_limit += 1
			program.append(INSTR_STORE)
			program.append(int(line.strip("STORE ")))
		elif line[:3] == "POP":
			stack_limit -= 1
			program.append(INSTR_POP)
			program.append(0)
		
		max_stack_limit = max(max_stack_limit, stack_limit)
		max_memory_limit = max(max_memory_limit, memory_limit)
					
		counter +=1
	
	stack = Stack(max_stack_limit)
	memory = Memory(max_memory_limit)
	execute(program, stack, memory)


def max(a, b):
	if a > b:
		return a
	else:
		return b

def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "You must supply a filename"
        return 1
    
    run(os.open(filename, os.O_RDONLY, 0777))
    return 0

def target(*args):
    return entry_point, None
    
def jitpolicy(driver):
	from rpython.jit.codewriter.policy import JitPolicy
	return JitPolicy()

if __name__ == "__main__":
    entry_point(sys.argv)

