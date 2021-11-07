# Symbol Map: accessor for data in a dolphin format symbol map

class SymbolMap:
    def __init__(self, path, cpp_macros):
        self.names = {}
        self.addresses = {}
        if path is not None:
            with open(path) as mapfile:
                for line in mapfile.readlines():
                    # addr size addr2 section(?) name
                    splt = line.split()
                    if len(splt) == 0:
                        continue
                    if not splt[0][0] == '8':
                        continue
                    addr = int(splt[0], 16)
                    name = splt[4]
                    self.names[addr] = name
                    self.addresses[name] = addr
        self.cpp_macros = cpp_macros

    def has_name(self, addr):
        return addr in self.names

    def has_address(self, name):
        return name in self.addresses

    def get_name(self, addr):
        if self.has_name(addr):
            return self.names[addr]
        else:
            if self.cpp_macros:
                return f"unk_{addr:x}"
            else:
                return hex(addr)
    
    def get_address(self, name):
        return self.addresses[name]
