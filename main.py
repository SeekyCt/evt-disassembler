from config import config
from binread import BinaryReader 
from opcodes import opcodes, opcodesR
from parsers import parsers, getIndent, getUnindent

ptr = config.addr
if config.toFile:
    out = open(config.outPath, 'w')
f = BinaryReader.getStaticInstance()

opc = 0
indent = 0
indentNext = 0
while opc != opcodesR["end_script"]:
    # halfword    cmdn
    # halfword    cmd
    # word[cmdn]  data
    count = f.readatH(ptr)
    opc = f.readatH(ptr + 2)
    data = f.readatWA(ptr + 4, count)

    line = f"{opcodes[opc]} {parsers[opc](data)}"
    indent += getUnindent(opc)
    if indent < 0:
        indent = 0 # sometimes the game put too many end_ifs
    line = '    ' * indent + line
    indent += getIndent(opc)

    if config.showLineAddrs:
        line = f"{hex(ptr)[2:]}: {line}"
    if config.toFile:
        out.write(line + '\n')
    else:
        print(line)

    ptr += 4 + (count * 4)

if config.toFile:
    out.close()
BinaryReader.destroyStaticInstance()