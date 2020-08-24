from config import Config
from binread import BinaryReader 
from opcodes import opcodes, opcodesR
from parsers import parsers

config = Config.getStaticInstance()
ptr = config.addr
if config.toFile:
    out = open(config.outPath, 'w')
f = BinaryReader.getStaticInstance()

opc = 0
while opc != opcodesR["end_script"]:
    # halfword    cmdn
    # halfword    cmd
    # word[cmdn]  data
    count = f.readatH(ptr)
    opc = f.readatH(ptr + 2)
    data = f.readatWA(ptr + 4, count)

    line = f"{opcodes[opc]} {parsers[opc](data)}"
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
Config.destroyStaticInstance()