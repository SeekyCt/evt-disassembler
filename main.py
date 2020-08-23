from config import Config
from binread import BinaryReader 
from opcodes import opcodes, opcodesR
from parsers import parsers

def output(msg):
    if config.toFile:
        out.write(msg + '\n')
    else:
        print(msg)

config = Config.getStaticInstance()
ptr = config.addr
if config.toFile:
    out = open(config.outPath, 'w')
f = BinaryReader.getStaticInstance()

opc = 0
while opc != opcodesR["end_script"]:
    # halfword    cmd
    # halfword    cmdn
    # word[cmdn]  data
    count = f.readatH(ptr)
    opc = f.readatH(ptr + 2)
    data = f.readatWA(ptr + 4, count)

    if config.showLineAddrs:
        output(f"{hex(ptr)[2:]}: {opcodes[opc]} {parsers[opc](data)}")
    else:
        output(f"{opcodes[opc]} {parsers[opc](data)}")

    ptr += 4 + (count * 4)

if config.toFile:
    out.close()
BinaryReader.destroyStaticInstance()