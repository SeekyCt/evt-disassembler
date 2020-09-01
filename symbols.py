from config import Config

class SymbolMap:
    _sInstance = None
    @staticmethod
    def getStaticInstance():
        if SymbolMap._sInstance is None:
            SymbolMap._sInstance = SymbolMap(Config.getStaticInstance().mapPath)
        return SymbolMap._sInstance
    @staticmethod
    def destroyStaticInstance():
        del SymbolMap._sInstance

    def __init__(self, path):
        mapfile = open(path, 'r')
        self._addrToName = {}
        self._nameToAddr = {}    
        for line in mapfile.readlines():
            # addr size addr2 section(?) name
            splt = line.split()
            if len(splt) == 0:
                continue
            addr = splt[0]
            if not splt[0][0] == '8':
                continue
            name = line[line.find(splt[4]):-1] # name can contain spaces so we can't just use split()
            self._addrToName[addr] = name
            self._nameToAddr[name] = addr
        mapfile.close()

    def getName(self, addr):
        return self._addrToName[addr]
    
    def getAddress(self, name):
        return self._nameToAddr[name]