import argparse

class Config:
    _sInstance = None
    @staticmethod
    def getStaticInstance():
        if Config._sInstance is None:
            Config._sInstance = Config()
        return Config._sInstance
    @staticmethod
    def destroyStaticInstance():
        del Config._sInstance

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--ramfile", "-r")
        parser.add_argument("--outfile", "-o")
        parser.add_argument("--address", "-a")
        parser.add_argument("--showstrings", "-s", action="store_true")
        parser.add_argument("--lineaddrs", "-l", action="store_true")
        parser.add_argument("--nopointer", '-n', action="store_true")
        args = parser.parse_args()

        # --ramfile path, -r path
        # Path to the MEM1 RAM dump
        if args.ramfile is not None:
            self.dumpPath = args.ramfile
        else:
            self.dumpPath = "ram.raw"
        
        # --outfile path, -o path
        # Disassembly is stored to a text file instead of being printed to the console
        if args.outfile is not None:
            self.toFile = True
            self.outPath = args.outfile
        else:
            self.toFile = False
            self.outPath = None

        # --address addr, -a addr
        # Address of the script to disassemble
        # Ex. 80e4a688 for aa1_01_init_evt
        if args.address is not None:
            if args.address.startswith('0x'):
                args.address = args.address[2:]
            self.addr = int(args.address, 16)
        else:
            self.addr = int(input("addr: 0x"), 16)

        # --showstrings, -s
        # Prints the contents of a string instead of its address for supported instructions, currently can't re-assemble
        #   enabled:  debug_put_msg "aa1_01_init_evt"
        #   disabled: debug_put_msg 80CAC958
        self.showStrings = args.showstrings

        # --lineaddrs, -l
        # Prints the memory address of an instruction at the start of the line
        #   enabled:  80e4a688: debug_put_msg 0x80CAC958
        #   disabled: debug_put_msg 0x80CAC958
        self.showLineAddrs = args.lineaddrs

        # --nopointer, -n
        # Prints 'ptr' instead of actual addresses, useful for comparing code from different builds
        #   enabled:  user_func ptr, 1, 1, ptr, 1073741824
        #   disabled: user_func 0x800eb72c, 1, 1, 0x80caa0d0, 1073741824
        self.noPointer = args.nopointer