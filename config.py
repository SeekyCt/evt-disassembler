import argparse

class Config:
    _sInstance = None
    @staticmethod
    def getStaticInstance():
        if Config._sInstance is None:
            Config._sInstance = Config()
        return Config._sInstance

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--ramfile", "-r")
        parser.add_argument("--outfile", "-o")
        parser.add_argument("--straddrs", "-s", action="store_true")
        parser.add_argument("--lineaddrs", "-l", action="store_true")
        args = parser.parse_args()

        # --straddrs, -s
        # Prints the memory address of a string after it
        #   enabled:  "aa1_01_init_evt"_80CAC958
        #   disabled: "aa1_01_init_evt"
        self.showStrAddrs = args.straddrs

        # --lineaddrs, -l
        # Prints the memory address of an instruction at the start of the line
        #   enabled:  80e4a688: debug_put_msg "aa1_01_init_evt"
        #   disabled: debug_put_msg "aa1_01_init_evt"
        self.showLineAddrs = args.lineaddrs

        # --outfile=path, -o path
        # Disassembly is stored to a text file instead of being printed to the console
        if args.outfile is not None:
            self.toFile = True
            self.outPath = args.outfile
        else:
            self.toFile = False
            self.outPath = None

        # --ramfile=path, -r path
        # Path to the MEM1 RAM dump
        if args.ramfile is not None:
            self.dumpPath = args.ramfile
        else:
            self.dumpPath = "ram.raw"