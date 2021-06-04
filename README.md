# Evt Script Disassembler
A disassembler for binary evt scripts in a Super Paper Mario RAM dump

For most people this doesn't really offer any advantages over ttydasm, I mostly just made this for fun and also to make certain things easier to automate for myself

## Usage
Either run main.py and it will prompt you to enter the script's memory address, or use the command line arguments (recommended)

### --ramfile path, -r path
Path to the MEM1 RAM dump, defaults to 'ram.raw' in the current directory if not specified

### --outfile path, -o path
Path to the text file to store the result to (will print to console if not specified)

### --address addr, -a addr
Address of the script to disassemble, such as 80e4a688 for aa1_01_init_evt in PAL revision 0

### --map path, -m path
Replaces addresses with names from the symbol map file at the specified path where possible

Enabled (using a map with only dol addresses):

> user_func evt_mobj_save_blk, 0x80caa8a0, -200, 75, -275, 0x80d0dd60

Disabled:

> user_func 0x800fb118, 0x80caa8a0, -200, 75, -275, 0x80d0dd60

### --showstrings, -s
Prints the contents of a string instead of its address for supported instructions (currently not supported by evt-assembler)

Enabled:

> debug_put_msg "aa1_01_init_evt"

Disabled:

> debug_put_msg 80CAC958

### --lineaddrs, -l
Prints the memory address of an instruction at the start of the line

Enabled:

> 80e4a688: debug_put_msg 0x80CAC958

Disabled:

> debug_put_msg 0x80CAC958

### --nopointer, -n
Prints 'ptr' instead of actual addresses, useful for comparing code from different builds

Enabled:

> user_func ptr, 1, 1, ptr, 1073741824

Disabled:

> user_func 0x800eb72c, 1, 1, 0x80caa0d0, 1073741824

### --ttyd, -t
Changes opcodes and variable bases to their TTYD values

## Potential Update Plans
- More instruction-specific parsers (or maybe just removing the system entirely and doing some kind of string detection)

## Credits
This is heavily based off of the work by everyone involved in the creation of [ttyd-asm](https://github.com/PistonMiner/ttyd-tools)
