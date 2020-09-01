from config import config

class BinaryReader:
    _sInstance = None
    @staticmethod
    def getStaticInstance():
        if BinaryReader._sInstance is None:
            BinaryReader._sInstance = BinaryReader(config.dumpPath)
        return BinaryReader._sInstance
    @staticmethod
    def destroyStaticInstance():
        del BinaryReader._sInstance

    def __init__(self, path):
        self._f = open(path, 'rb')
    
    def __del__(self):
        self._f.close()

    def readat(self, addr, size):
        self._f.seek(addr - 0x80000000)
        return self._f.read(size)

    def readatS(self, addr):
        self._f.seek(addr - 0x80000000)
        strn = ""
        while True:
            c = self._f.read(1)[0]
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
    
    def readatWA(self, addr, length):
        return [self.readatW(addr + (i * 4)) for i in range(0, length)]