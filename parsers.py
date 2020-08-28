import struct
from config import Config
from binread import BinaryReader
from opcodes import opcodes, opcodesR

indents = ["do", "if_str_equal", "if_str_not_equal", "if_str_small", "if_str_large", "if_str_small_equal", "if_str_large_equal", "iff_equal", "iff_not_equal", "iff_small", "iff_large", "iff_small_equal", "iff_large_equal", "if_equal", "if_not_equal", "if_small", "if_large", "if_small_equal", "if_large_equal", "if_flag", "if_not_flag", "inline_evt", "inline_evt_id", "brother_evt", "brother_evt_id"]
unindents = ["end_if", "end_inline", "while", "end_brother"]
middleindents = ["else", "case", "case_equal", "case_not_equal", "case_small", "case_large", "case_small_equal", "case_large_equal", "case_etc", "case_or", "case_and", "case_flag", "case_between"]
indents += middleindents
unindents += middleindents

def getUnindent(opc):
    if opcodes[opc] == "end_switch":
        return -2
    else:
        return -1 * (opcodes[opc] in unindents)

def getIndent(opc):
    if opcodes[opc] in ["switch", "switchi"]:
        return 2
    else:
        return opcodes[opc] in indents

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
                return t
        elif t == 'Float':
            if val < typeBases['UF']:
                return t
        else:
            base = typeBases[t]
            if base <= val <= base + 10000000:
                return t
    return "Immediate"

def normalOperand(val):
    sval = struct.unpack(">i", int.to_bytes(val, 4, 'big'))[0]
    t = getType(sval)
    if t == 'Address':
        if Config.getStaticInstance().nopointer:
            return "ptr"
        else:
            return hex(val)
    if t == 'Float':
        return f"{(sval - typeBases['Float']) / 1024}"
    if t == 'Immediate':
        return sval
    return f"{t}({sval - typeBases[t]})"

def stringOperand(addr):
    if Config.getStaticInstance().showStrings:
        f = BinaryReader.getStaticInstance()
        return f'"{f.readatS(addr)}"'
    else:
       return hex(addr)

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
setParser("if_str_equal", parseIfStrEqual)