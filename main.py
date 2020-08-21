import config
from binread import BinaryReader 
from opcodes import opcodes, opcodesR
from parsers import parsers

# ex. 80e4a688 for aa1_01_init_evt
ptr = int(input("addr: 0x"), 16)
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
        print(f"{hex(ptr)[2:]}: {opcodes[opc]} {parsers[opc](data)}")
    else:
        print(f"{opcodes[opc]} {parsers[opc](data)}")

    ptr += 4 + (count * 4)