from stack import *
print("RPN Calculator - Console\n")
pilha = Stack()
while True:
    s=input("Enter with a number ('q' to quit):")        
    if s == '+':
        n1 = pilha.pop()
        n2 = pilha.pop()
        pilha.push(float(n1)+float(n2))
        pilha.show()
    if s == "-":
        n1 = pilha.pop()
        n2 = pilha.pop()
        pilha.push(float(n1) - float(n2))
        pilha.show()
    if s == "*":
        n1 = pilha.pop()
        n2 = pilha.pop()
        pilha.push(float(n1)*float(n2))
        pilha.show()
    if s == "/":
        n1 = pilha.pop()
        n2 = pilha.pop()
        pilha.push(float(n1)/float(n2))
        pilha.show()
    if s[0]=='q':
        break
    if s.isnumeric()==True:
        pilha.push(float(s))
pilha.show()

