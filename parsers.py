import config
from binread import BinaryReader
from opcodes import opcodesR

def setParser(opName, parser):
    parsers[opcodesR[opName]] = parser

def parseDefault(data):
    if len(data) == 0:
        return ""
    s = "["
    for d in data:
        s += f"{hex(d)}, "
    return s[:-2] + "]"

def parseDebugPutMsg(data):
    addr = data[0]
    f = BinaryReader.getStaticInstance()
    if config.showStrAddrs:
        return f'"{f.readatS(addr)}"_{hex(addr)[2:]}'
    else:
        return f'"{f.readatS(addr)}"'

parsers = {}
for i in range(0, 119):
    parsers[i] = parseDefault
setParser("debug_put_msg", parseDebugPutMsg)