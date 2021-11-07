# Binary Reader: reads binary data from a RAM dump into various forms

from typing import List

class BinaryReader:
    def __init__(self, path: str):
        with open(path, 'rb') as f:
            self.dat = f.read()

    # Address to ram dump offset
    def addr_to_offs(self, addr: int) -> int:
        return addr - 0x80000000

    # Reads bytes at an address 
    def read(self, addr: int, size: int) -> bytes:
        offs = self.addr_to_offs(addr)
        return self.dat[offs:offs+size]

    # Reads a null-terminated SJIS string at an address
    def read_str(self, addr: int) -> str:
        offs = self.addr_to_offs(addr)
        strn = bytearray()
        while True:
            c = self.dat[offs]
            if c == 0:
                break
            strn.append(c)
            offs += 1
        return strn.decode("shift-jis")

    # Reads an integer at an address
    def read_int(self, addr: int, size: int) -> int:
        return int.from_bytes(self.read(addr, size), "big")

    # Reads a halfword at an address
    def read_half(self, addr: int) -> int:
        return self.read_int(addr, 2)

    # Reads a word at an address
    def read_word(self, addr: int) -> int:
        return self.read_int(addr, 4)
    
    # Reads a word array at an address
    def read_word_array(self, addr: int, length: int) -> List[int]:
        return [self.read_word(addr + (i * 4)) for i in range(length)]
