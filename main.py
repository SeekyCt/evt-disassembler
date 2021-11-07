from config import Config
from disassembler import Disassembler

def main():
    ctx = Config()
    dis = Disassembler(ctx)
    txt = dis.disassemble(ctx.addr)
    print(txt)

if __name__ == "__main__":
    main()
