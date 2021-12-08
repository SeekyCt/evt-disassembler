# Disassembler: converts binary evt scripts to text

from binread import BinaryReader
from config import Config
from opcodes import OpcodeNamer
from symbols import SymbolMap

from enum import Enum
import struct

class Indenter:
    def __init__(self, namer: OpcodeNamer):
        self.opc = namer

        # Indentation definitions
        # Unindentation happens before instruction, indentation after
        # "Middle" indents unindent before and indent after
        self.indents = {
            "do", "if_str_equal", "if_str_not_equal", "if_str_small", "if_str_large",
            "if_str_small_equal", "if_str_large_equal", "iff_equal", "iff_not_equal",
            "iff_small", "iff_large", "iff_small_equal", "iff_large_equal", "if_equal",
            "if_not_equal", "if_small", "if_large", "if_small_equal", "if_large_equal",
            "if_flag", "if_not_flag", "inline_evt", "inline_evt_id", "brother_evt",
            "brother_evt_id"
        }
        self.double_indents = {
            "switch", "switchi"
        }
        self.middle_indents = {
            "else", "case", "case_equal", "case_not_equal", "case_small", "case_large",
            "case_small_equal", "case_large_equal", "case_etc", "case_or", "case_and",
            "case_flag", "case_between"
        }
        self.unindents = {
            "end_if", "end_inline", "while", "end_brother"
        }
        self.double_unindents = {
            "end_switch"
        }
        self.indents |= self.middle_indents
        self.unindents |= self.middle_indents

    # Opcode to indentation difference before instruction
    def get_unindent(self, opc: int) -> int:
        if self.opc.opc_to_name(opc) in self.double_unindents:
            return 2
        elif self.opc.opc_to_name(opc) in self.unindents:
            return 1
        else:
            return 0

    # Opcode to indentation difference after instruction
    def get_indent(self, opc: int) -> int:
        if self.opc.opc_to_name(opc) in self.double_indents:
            return 2
        elif self.opc.opc_to_name(opc) in self.indents:
            return 1
        else:
            return 0

class OpType(Enum):
    NORMAL = 0
    STRING = 1
    HEX = 2
    FUNC = 3

class Disassembler:
    def __init__(self, ctx: Config):
        self.ctx = ctx
        self.opc = OpcodeNamer(self.ctx.spm, self.ctx.cpp_macros)
        self.ram = BinaryReader(self.ctx.dump_path)
        self.sym = SymbolMap(self.ctx.map_path, self.ctx.cpp_macros)
        self.idt = Indenter(self.opc)

        # Special disassembly for certain operands
        self.operand_type_defs = {
            "if_str_equal"       : [OpType.STRING, OpType.STRING],
            "if_str_not_equal"   : [OpType.STRING, OpType.STRING],
            "if_str_small"       : [OpType.STRING, OpType.STRING],
            "if_str_large"       : [OpType.STRING, OpType.STRING],
            "if_str_small_equal" : [OpType.STRING, OpType.STRING],
            "if_str_large_equal" : [OpType.STRING, OpType.STRING],
            "if_flag"            : [OpType.HEX,    OpType.HEX],
            "if_not_flag"        : [OpType.HEX,    OpType.HEX],
            "case_flag"          : [OpType.HEX],
            "debug_put_msg"      : [OpType.STRING],
            "user_func"          : [OpType.FUNC]
        }

        # Data type definitions
        self.type_bases = {
            "Address" : -270000000,
            "Float" : -240000000,
            "UF" : -210000000,
            "UW" : -190000000,
            "GSW" : -170000000,
            "LSW" : -150000000,
            "GSWF" : -130000000,
            "LSWF" : -110000000,
            "GF" : -90000000,
            "LF" : -70000000,
            "GW" : -50000000,
            "LW" : -30000000
        }
        if not self.ctx.spm:
            self.type_bases["Address"] = -250000000
            self.type_bases["Float"] = -230000000

    # Disassembles a script at an address
    def disassemble(self, addr: int) -> str:
        # Indent inside EVT_BEGIN block for macro mode
        if self.ctx.cpp_macros:
            lines = [f"EVT_BEGIN({self.sym.get_name(addr)})"]
            min_indent = 1
            indent = 1
        else:
            lines = []
            min_indent = 0
            indent = 0

        # Disassemble
        ptr = addr
        opc = 2 # any valid value that isn't end_script
        while self.opc.opc_to_name(opc) != "end_script":
            # halfword    cmdn
            # halfword    cmd
            # word[cmdn]  data
            count = self.ram.read_half(ptr)
            opc = self.ram.read_half(ptr + 2)
            data = self.ram.read_word_array(ptr + 4, count)

            # Convert line to text
            line = self.disassemble_line(opc, data)

            # Unindent before instruction
            # Limited with min_indent since the game sometimes puts too many end_if opcodes
            indent -= self.idt.get_unindent(opc)
            indent = max(min_indent, indent)

            # Macro mode needs to fully unindent when terminating
            if self.ctx.cpp_macros and self.opc.opc_to_name(opc) == "end_script":
                indent = 0

            # Apply indentation to line
            line = "    " * indent + line

            # Indent after instruction
            indent += self.idt.get_indent(opc)

            # Add address if enabled
            if self.ctx.show_line_addrs:
                line = f"{hex(ptr)[2:]}: {line}"
            
            # Append to output
            lines.append(line)

            # Move to next instruction
            ptr += 4 + (count * 4)
        
        return '\n'.join(lines)

    # Int to datatype
    def get_type(self, val: int) -> int:
        for t in self.type_bases:
            # Special extent for address and float
            if t == "Address":
                if val <= self.type_bases[t]:
                    return t
            elif t == "Float":
                if val < self.type_bases["UF"]:
                    return t
            else:
                base = self.type_bases[t]
                if base <= val <= base + 10000000:
                    return t
        return "Immediate"

    # Uint to int
    def sign(self, val: int) -> int:
        return struct.unpack(">i", int.to_bytes(val, 4, "big"))[0]

    # Prints an address
    def format_addr(self, addr: int) -> str:
        if self.sign(addr) == self.type_bases["Address"]:
            # ADDR(0) is used as a null pointer for some functions
            if self.ctx.cpp_macros:
                return "EVT_NULLPTR"
            else:
                return "nullptr"
        else:
            if self.ctx.no_pointer and not self.sym.has_name(addr):
                # Hide bare addresses in noPointer mode
                return "ptr"
            else:
                # Return symbol instead of address if known
                return self.sym.get_name(addr)
                
    # Prints an operand
    def operand_normal(self, val: int) -> str:
        sval = self.sign(val)
        t = self.get_type(sval)
        if t == "Address":
            return self.format_addr(val)
        elif t == "Float":
            return str((sval - self.type_bases["Float"]) / 1024)
        elif t == "Immediate":
            return str(sval)
        else:
            return f"{t}({sval - self.type_bases[t]})"

    # Prints a string address as its value if enabled
    def operand_string(self, addr: int) -> str:
        t = self.get_type(self.sign(addr))
        if t == "Address" and self.ctx.show_strings:
            return f'"{self.ram.read_str(addr)}"'
        else:
            return self.operand_normal(addr)
    
    # Prints an immediate in hex (for flags)
    def operand_hex(self, val: int) -> str:
        t = self.get_type(self.sign(val))
        if t == "Immediate":
            return hex(val)
        else:
            return self.operand_normal(val)
    
    # Disassembles one operand of a line
    def disassemble_operand(self, val: int, op_t: OpType):
        # Format based on type
        if op_t == OpType.STRING:
            ret = self.operand_string(val)
        elif op_t == OpType.HEX:
            ret = self.operand_hex(val)
        else: # including OpType.FUNC, handled later
            ret = self.operand_normal(val)
        
        # Add extra macro formatting if needed
        if self.ctx.cpp_macros and op_t != OpType.FUNC:
            val_t = self.get_type(self.sign(val))
            if val_t == "Address" and self.sign(val) != self.type_bases["Address"]:
                if op_t == OpType.STRING:
                    ret = f"PTR({ret})"
                else:
                    ret = f"PTR(&{ret})"
            elif val_t == "Float":
                ret = f"FLOAT({ret})"

        return ret;        

    # Disassembles one line of a script
    def disassemble_line(self, opc, data):
        # Add instruction name
        instr = self.opc.opc_to_name(opc)
        line = f"{self.opc.name_to_printing_name(instr)}"

        # Add operands
        if len(data) > 0:
            # Get operand type definitions
            if instr in self.operand_type_defs:
                types = self.operand_type_defs[self.opc.opc_to_name(opc)][:len(data)]
            else:
                types = []

            # Default to normal operand if not defined
            if len(types) < len(data):
                types += [OpType.NORMAL for _ in range(len(data) - len(types))]

            # Format each operand by type
            ops = [self.disassemble_operand(data[i], t) for i, t in enumerate(types)]
        else:
            ops = []

        if self.ctx.cpp_macros:
            line += '(' + ", ".join(ops) + ')'
        else:
            line += ' ' + ", ".join(ops)

        return line.strip()
