from config import config

class SymbolMap:
    def __init__(self, path):
        mapfile = open(path, 'r')
        self._addrToName = {}
        self._nameToAddr = {}    
        for line in mapfile.readlines():
            # addr size addr2 section(?) name
            splt = line.split()
            if len(splt) == 0:
                continue
            if not splt[0][0] == '8':
                continue
            addr = int(splt[0], 16)
            name = splt[4]
            #name = line[line.find(splt[4]):-1] # name can contain spaces so we can't just use split()
            self._addrToName[addr] = name
            self._nameToAddr[name] = addr
        mapfile.close()

    def hasAddress(self, addr):
        return addr in self._addrToName

    def getName(self, addr):
        return self._addrToName[addr]
    
    def getAddress(self, name):
        return self._nameToAddr[name]

if config.useMap:
    symbolMap = SymbolMap(config.mapPath)
else:
    symbolMap = None