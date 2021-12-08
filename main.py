from sys import stdout
from config import Config
from disassembler import Disassembler

def main():
    ctx = Config()
    dis = Disassembler(ctx)
    txt = dis.disassemble(ctx.addr)
    stdout.buffer.write(txt.encode("utf8")) # TODO: is there a better way to fix this?

if __name__ == "__main__":
    main()
