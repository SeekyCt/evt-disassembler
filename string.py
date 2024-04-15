from sys import stdout
from binread import BinaryReader
from config import Config

def main():
    ctx = Config()
    ram = BinaryReader(ctx.dump_path)
    txt = ram.read_str(ctx.addr)
    stdout.buffer.write(txt.encode("utf8")) # TODO: is there a better way to fix this?
    x = input()
if __name__ == "__main__":
    main()