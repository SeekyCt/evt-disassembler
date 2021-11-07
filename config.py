# Config: command line arguments for the program

import argparse

class Config:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--ramfile", "-r")
        parser.add_argument("--address", "-a")
        parser.add_argument("--map", "-m")
        parser.add_argument("--showstrings", "-s", action="store_true")
        parser.add_argument("--lineaddrs", "-l", action="store_true")
        parser.add_argument("--nopointer", '-n', action="store_true")
        parser.add_argument("--ttyd", "-t", action="store_true")
        parser.add_argument("--cpp", "-c", action="store_true")
        args = parser.parse_args()

        # --ramfile path, -r path
        # Path to the MEM1 RAM dump
        if args.ramfile is not None:
            self.dump_path = args.ramfile
        else:
            self.dump_path = "ram.raw"

        # --address addr, -a addr
        # Address of the script to disassemble
        # Ex. 80e4a688 for aa1_01_init_evt
        if args.address is not None:
            self.addr = int(args.address, 16)
        else:
            self.addr = int(input("addr: "), 16)

        # --map path, -m path
        # Path to a symbol map, will be used 
        # Ex. 80e4a688 for aa1_01_init_evt
        if args.map is not None:
            self.map_path = args.map
        else:
            self.map_path = None

        # --showstrings, -s
        # Prints the contents of a string instead of its address for supported instructions, currently can't re-assemble
        #   enabled:  debug_put_msg "aa1_01_init_evt"
        #   disabled: debug_put_msg 80CAC958
        self.show_strings = args.showstrings

        # --lineaddrs, -l
        # Prints the memory address of an instruction at the start of the line
        #   enabled:  80e4a688: debug_put_msg 0x80CAC958
        #   disabled: debug_put_msg 0x80CAC958
        self.show_line_addrs = args.lineaddrs

        # --nopointer, -n
        # Prints 'ptr' instead of actual addresses, useful for comparing code from different builds
        #   enabled:  user_func ptr, 1, 1, ptr, 1073741824
        #   disabled: user_func 0x800eb72c, 1, 1, 0x80caa0d0, 1073741824
        self.no_pointer = args.nopointer

        # --ttyd, -t
        # Changes to TTYD values for opcodes and vriables
        self.spm = not args.ttyd

        # --cpp, -c
        # Changes output format to C++ preprocessor macros
        self.cpp_macros = args.cpp
