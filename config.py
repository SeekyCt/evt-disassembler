# TODO: move this to command line args

# Prints the memory address of a string after it
#   enabled:  "aa1_01_init_evt"_80CAC958
#   disabled: "aa1_01_init_evt"
showStrAddrs = False

# Prints the memory address of an instruction at the start of the line
#   enabled:  80e4a688: debug_put_msg "aa1_01_init_evt"
#   disabled: debug_put_msg "aa1_01_init_evt"
showLineAddrs = True 

# Disassembly is stored to a text file instead of being printed to the console
toFile = False # outputs to out.txt instead of console

# Path to the text file to use when toFile is enabled
outPath = "out.txt"

# Path to the MEM1 RAM dump
dumpPath = "ram.raw" 