import os
import sys

try:
    from rpython.rlib.jit import JitDriver
except ImportError:
    class JitDriver(object):
        def __init__(self,**kw): pass
        def jit_merge_point(self,**kw): pass
        def can_enter_jit(self,**kw): pass
        

            
jitdriver = JitDriver(greens=['pc', 'program'], reds=['stack'])

def execute(program, stack_limit):
	stack = Stack(stack_limit)
	pc = 0
	while pc < len(program):
		jitdriver.jit_merge_point(pc=pc, program=program,
                stack=stack)
    #ADD=0, SUB=1, PRINT=2, JUMP=3, INT=4, JNZERO = 5, FIB = 6
		line = program[pc]
		
		if line == 0:
			result = (stack.pop() + stack.pop())
			stack.push(result)
			pc += 2
		elif line == 1:
			result = stack.pop() - program[pc + 1]
			stack.push(result)
			pc += 2
		elif line == 2:
			output = stack.pop()
			print output
			pc += 2
		elif line == 3:
			pc = (program[pc + 1] * 2)
		elif line == 4:
			stack.push(program[pc + 1])
			pc += 2
		elif line == 5:
			if stack.stack[stack.pointer - 1] != 0:
				pc = (program[pc + 1] * 2)
			else:
				pc += 2
		elif line == 6:
			x = fib(program[pc + 1])
			stack.push(x)
			pc += 2


def fib(number):
	if number == 1 or number == 2:
		return 1
	else:
		fibonacci = 0
		a = 1
		b = 1
		counter = 3
		while counter < number:
			fibonacci = a + b
			a = b
			b = fibonacci
			counter += 1
		return fibonacci

class Stack:
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
    #ADD=0, SUB=1, PRINT=2, JUMP=3, INT=4, JNZERO = 5, FIB 6
	counter = 0
	stack_limit = 0
	program = []
    
	while counter < len(p):
   		line = p[counter]
		if line[:3] == "ADD":
			program.append(0)
			program.append(0)			
		elif line[:3] == "INT":
			stack_limit += 1
			program.append(4)
			program.append(int(line.strip("INT ")))
		elif line[:4] == "JUMP":
			program.append(3)
			program.append(int(line.strip("JUMP ")))
		elif line[:3] == "SUB":
			program.append(1)
			program.append(int(line.strip("SUB ")))
		elif line[:6] == "JNZERO":
			program.append(5)
			program.append(int(line.strip("JNZERO ")))
		elif line[:5] == "PRINT":
			program.append(2)
			program.append(0)
		elif line[:3] == "FIB":
			stack_limit += 1
			program.append(6)
			program.append(int(line.strip("FIB ")))
		counter +=1
	execute(program, stack_limit)


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

