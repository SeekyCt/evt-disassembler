import struct
from enum import Enum
from config import config
from binread import ramReader
from opcodes import opcodes, opcodesR
from symbols import symbolMap

# Indentation definitions
indents = ["do", "if_str_equal", "if_str_not_equal", "if_str_small", "if_str_large", "if_str_small_equal", "if_str_large_equal", "iff_equal", "iff_not_equal", "iff_small", "iff_large", "iff_small_equal", "iff_large_equal", "if_equal", "if_not_equal", "if_small", "if_large", "if_small_equal", "if_large_equal", "if_flag", "if_not_flag", "inline_evt", "inline_evt_id", "brother_evt", "brother_evt_id"]
doubleIndents = ["switch", "switchi"]
middleIndents = ["else", "case", "case_equal", "case_not_equal", "case_small", "case_large", "case_small_equal", "case_large_equal", "case_etc", "case_or", "case_and", "case_flag", "case_between"]
unindents = ["end_if", "end_inline", "while", "end_brother"]
doubleUnindents = ["end_switch"]
indents += middleIndents
unindents += middleIndents

# Special disassembly for certain operands
class OpType(Enum):
    NORMAL = 0
    STRING = 1
    HEX = 2
operandTypeDefs = {
    "if_str_equal"       : [OpType.STRING, OpType.STRING],
    "if_str_not_equal"   : [OpType.STRING, OpType.STRING],
    "if_str_small"       : [OpType.STRING, OpType.STRING],
    "if_str_large"       : [OpType.STRING, OpType.STRING],
    "if_str_small_equal" : [OpType.STRING, OpType.STRING],
    "if_str_large_equal" : [OpType.STRING, OpType.STRING],
    "if_flag"            : [OpType.HEX,    OpType.HEX],
    "if_not_flag"        : [OpType.HEX,    OpType.HEX],
    "case_flag"          : [OpType.HEX],
    "debug_put_msg"      : [OpType.STRING]
}

# Data type definitions
if config.spm:
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
else:
    typeBases = {
        'Address': -250000000,
        'Float': -230000000,
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

# Opcode to indentation difference before instruction (-2, -1, 0)
def getUnindent(opc):
    if opcodes[opc] in doubleUnindents:
        return -2
    else:
        return -1 * (opcodes[opc] in unindents)

# Opcode to indentation difference after instruction (0, 1, 2)
def getIndent(opc):
    if opcodes[opc] in doubleIndents:
        return 2
    else:
        return opcodes[opc] in indents

# Uint to int
def sign(val):
    return struct.unpack(">i", int.to_bytes(val, 4, 'big'))[0]

# Int to datatype
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

# Normal disassembler for operands
def normalOperand(val):
    sval = sign(val)
    t = getType(sval)
    if t == 'Address':
        if sval == typeBases[t]:
            return "nullptr"
        else:
            if config.useMap and symbolMap.hasAddress(val):
                return symbolMap.getName(val)
            elif config.noPointer:
                return "ptr"
            else:
                return hex(val)
    elif t == 'Float':
        return f"{(sval - typeBases['Float']) / 1024}"
    elif t == 'Immediate':
        return sval
    else:
        return f"{t}({sval - typeBases[t]})"

# Print a string address as its value
def stringOperand(addr):
    t = getType(sign(addr))
    if t == 'Address':
        if config.showStrings:
            return f'"{ramReader.readatS(addr)}"'
        elif config.noPointer:
            return "ptr"
        else:
            return hex(addr)
    else:
        return normalOperand(addr)

# Print immediates in hex (for flags)
def hexOperand(val):
    t = getType(sign(val))
    if t == 'Immediate':
        return hex(val)
    else:
        return normalOperand(val)    

# Disassemble an operand list for a specific instruction
def parseOperands(opc, data):
    if len(data) == 0:
        return ""
    
    s = ""

    instr = opcodes[opc]
    if instr in operandTypeDefs:
        types = operandTypeDefs[opcodes[opc]]
        for i, t in enumerate(types):
            if i >= len(data):
                break
            if t == OpType.STRING:
                s += f"{stringOperand(data[i])}, "
            elif t == OpType.HEX:
                s += f"{hexOperand(data[i])}, "
            else:
                s += f"{normalOperand(data[i])}, "
    else:
        i = -1

    for d in data[i+1:]:
        s += f"{normalOperand(d)}, "

    return s[:-2]
