import struct
from enum import Enum, auto
from config import Config
from binread import BinaryReader
from opcodes import opcodesR

class DataTypes(Enum):
    Address = "Address"
    Float = "Float"
    UF = "UF"
    UW = "UW"
    GSW = "GSW"
    LSW = "LSW"
    GSWF = "GSWF"
    LSWF = "LSWF"
    GF = "GF"
    LF = "LF"
    GW = "GW"
    LW = "LW"
    Immediate = "Immediate"

typeBases = {
    'Address': -270000000,
    'Float': -240000000,
    'UF': -210000000,
    'UW': -190000000,
    'GSW': -170000000,
    'LSW': -150000000,
    'GSWF': -130000000,
    'LSWF': -110000000,
    'GF': -90000000,
    'LF': -70000000,
    'GW': -50000000,
    'LW': -30000000
}

def getType(val):
    for t in typeBases:
        if t == 'Address':
            if val <= typeBases[t]:
                return DataTypes.Address
        elif t == 'Float':
            if val < typeBases['UF']:
                return DataTypes.Float
        else:
            base = typeBases[t]
            if base <= val <= base + 10000000:
                return DataTypes[t]
    return DataTypes.Immediate

def normalOperand(val):
    sval = struct.unpack(">i", int.to_bytes(val, 4, 'big'))[0]
    t = getType(sval)
    if t == DataTypes.Address:
        return hex(val)
    if t == DataTypes.Float:
        return f"{(sval - typeBases['Float']) / 1024}f"
    if t == DataTypes.Immediate:
        return sval
    return f"{t.value}({sval - typeBases[t.value]})"

def stringOperand(addr):
    f = BinaryReader.getStaticInstance()
    s = f'"{f.readatS(addr)}"'
    if Config.getStaticInstance().showStrAddrs:
       s += f"_{hex(addr)[2:]}"
    return s

def parseDefault(data):
    if len(data) == 0:
        return ""
    s = ""
    for d in data:
        s += f"{normalOperand(d)}, "
    return s[:-2]

def parseDebugPutMsg(data):
    addr = data[0]
    return stringOperand(addr)

def parseIfStrEqual(data):
	return f"{normalOperand(data[0])}, {stringOperand(data[1])}"

def setParser(opName, parser):
    parsers[opcodesR[opName]] = parser

parsers = {}
for i in range(0, 119):
    parsers[i] = parseDefault
setParser("debug_put_msg", parseDebugPutMsg)
#setParser("if_str_equal", parseIfStrEqual)