class Stack:
    def __init__(self):
        self.top = 0
        self.elems = []
        for i in range(50):
            self.elems.append(0.0)

    def push(self,_n):
        self.elems[self.top] = _n
        self.top += 1

    def pop(self):
        self.top -= 1
        num = self.elems[self.top]
        return num

    def show(self):
        for i in range (0,self.top):
            print(self.elems[i])

    def save(self):
        arquivo=open("numeros.txt","w")
        for linha in range(1,101):
            arquivo.write("%d\n" % linha)
        arquivo.close()
