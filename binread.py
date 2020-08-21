class BinaryReader:
    sInstance = None
    @staticmethod
    def getStaticInstance():
        if BinaryReader.sInstance is None:
            BinaryReader.sInstance = BinaryReader("data/ram.raw")
        return BinaryReader.sInstance

    def __init__(self, path):
        self.f = open(path, 'rb')
    
    def __del__(self):
        self.f.close()

    def readat(self, addr, size):
        self.f.seek(addr - 0x80000000)
        return self.f.read(size)

    def readatS(self, addr):
        self.f.seek(addr - 0x80000000)
        strn = ""
        while True:
            c = self.f.read(1)[0]
            if c == 0:
                break
            strn += chr(c)
        return strn

    def readatI(self, addr, size):
        return int.from_bytes(self.readat(addr, size), 'big')

    def readatH(self, addr):
        return self.readatI(addr, 2)

    def readatW(self, addr):
        return self.readatI(addr, 4)
    
    def readatWA(self, addr, n):
        ret = []
        for i in range(0, n):
            ret.append(self.readatW(addr + (i * 4)))
        return ret