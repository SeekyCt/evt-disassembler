from config import config

class BinaryReader:
    def __init__(self, path):
        self._f = open(path, 'rb')
    
    def __del__(self):
        self._f.close()

    def readat(self, addr, size):
        self._f.seek(addr - 0x80000000)
        return self._f.read(size)

    def readatS(self, addr):
        self._f.seek(addr - 0x80000000)
        strn = bytearray()
        while True:
            c = self._f.read(1)[0]
            if c == 0:
                break
            strn.append(c)
        return strn.decode("shift-jis")

    def readatI(self, addr, size):
        return int.from_bytes(self.readat(addr, size), 'big')

    def readatH(self, addr):
        return self.readatI(addr, 2)

    def readatW(self, addr):
        return self.readatI(addr, 4)
    
    def readatWA(self, addr, length):
        return [self.readatW(addr + (i * 4)) for i in range(0, length)]

ramReader = BinaryReader(config.dumpPath)
