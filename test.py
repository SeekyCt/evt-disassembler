# Test: whole-program tests for various features

from dataclasses import dataclass
from disassembler import Disassembler
from symbols import SymbolMap

@dataclass
class DummyConfig:
    show_strings: bool
    show_line_addrs: bool
    no_pointer: bool
    cpp_macros: bool
    map_path: str
    dump_path: str
    spm: bool

def test_disasm(
    addr,
    show_strings = False,
    show_line_addrs = False,
    no_pointer = False,
    cpp_macros = False,
    map_path = "R8PP01.map",
    dump_path = "ram.raw",
    spm = True
):
    ctx = DummyConfig(show_strings, show_line_addrs, no_pointer, cpp_macros, map_path, dump_path, spm)
    dis = Disassembler(ctx)
    return dis.disassemble(addr)

# Lines with no operands
# Lines with operands
# String operands
# Indentation
# Named symbols
# Unnamed symbols
# String operands
# Line addresses
assert test_disasm(0x80d2f8c8, show_strings=True, show_line_addrs=True) == """80d2f8c8: user_func evt_sub_get_mapname, 0, LW(0)
80d2f8d8: if_str_equal LW(0), "mac_02"
80d2f8e4:     run_child_evt 0x80d2f650
80d2f8ec: end_if
80d2f8f0: if_str_equal LW(0), "mac_05"
80d2f8fc:     run_child_evt 0x80d2f718
80d2f904: end_if
80d2f908: if_str_equal LW(0), "mac_12"
80d2f914:     run_child_evt 0x80d2f788
80d2f91c: end_if
80d2f920: if_str_equal LW(0), "mac_15"
80d2f92c:     run_child_evt 0x80d2f858
80d2f934: end_if
80d2f938: end_evt
80d2f93c: end_script"""

# Double and middle indents
# No pointer
# Immediate operands
# No symbol map
assert test_disasm(0x80cf8f90, no_pointer=True, map_path=None) == """user_func ptr
switch GSW(0)
    case_between 174, 178
        user_func ptr, 1, 1, ptr, 1
    case_etc
        user_func ptr, 1, 1, ptr, 1
end_switch
set LW(0), 0
switch GSW(0)
    case_equal 59
        set LW(0), ptr
    case_equal 131
        set LW(0), ptr
    case_equal 288
        set LW(0), ptr
    case_large_equal 424
        if_equal GSWF(584), 0
            set LW(0), ptr
        end_if
end_switch
if_not_equal LW(0), 0
    do 0
        user_func ptr, 2, LW(1)
        if_not_flag LW(1), 0x1
            do_break
        end_if
        wait_frm 1
    while
    user_func ptr, 0
    run_evt LW(0)
end_if
end_evt
end_script"""

# Float operands
assert test_disasm(0x80cf8e28) == """mulf LW(0), 0.4443359375
user_func evt_mapobj_rotate, 0x80caa458, 0, LW(0), 0
mulf LW(0), -1.0
user_func evt_mapobj_rotate, 0x80caa460, 0, LW(0), 0
end_evt
end_script"""

# Hex operands
assert test_disasm(0x80d2b490) == """do 0
    user_func 0x800d4460, 0, LW(10)
    if_flag LW(10), 0x200
        do_break
    end_if
    user_func evt_key_get_buttontrg, 0, LW(10)
    if_flag LW(10), 0x300
        do_break
    end_if
    wait_frm 1
while
user_func 0x80c4af10, 2, LW(10)
if_flag LW(10), 0x4
    end_evt
end_if
user_func 0x80c4af10, 1, 2
user_func 0x80c4afc4, LW(0), 7, LW(10)
if_not_equal LW(10), 0
    run_child_evt LW(10)
end_if
user_func 0x800d231c, 0, 65, 500
user_func 0x800d3528, 0, 30, 500
user_func 0x800d3528, 1, 30, 500
user_func evt_snd_flag_on, 32
user_func 0x800e720c, 2, 1
user_func 0x800e7268, 1000, 300
user_func 0x80c4afc4, LW(0), 3, LW(1), LW(2)
user_func evt_seq_mapchange, LW(1), LW(2)
end_evt
end_script"""

# C++ macros
assert test_disasm(0x80d2f8c8, show_strings=True, cpp_macros=True) == """EVT_BEGIN()
    USER_FUNC(evt_sub_get_mapname, 0, LW(0))
    IF_STR_EQUAL(LW(0), PTR("mac_02"))
        RUN_CHILD_EVT(PTR(&unk_80d2f650))
    END_IF()
    IF_STR_EQUAL(LW(0), PTR("mac_05"))
        RUN_CHILD_EVT(PTR(&unk_80d2f718))
    END_IF()
    IF_STR_EQUAL(LW(0), PTR("mac_12"))
        RUN_CHILD_EVT(PTR(&unk_80d2f788))
    END_IF()
    IF_STR_EQUAL(LW(0), PTR("mac_15"))
        RUN_CHILD_EVT(PTR(&unk_80d2f858))
    END_IF()
    RETURN()
EVT_END()"""

# C++ macros with floats
assert test_disasm(0x80cf8e28, cpp_macros=True) == """EVT_BEGIN()
    MULF(LW(0), FLOAT(0.4443359375))
    USER_FUNC(evt_mapobj_rotate, PTR(&unk_80caa458), 0, LW(0), 0)
    MULF(LW(0), FLOAT(-1.0))
    USER_FUNC(evt_mapobj_rotate, PTR(&unk_80caa460), 0, LW(0), 0)
    RETURN()
EVT_END()"""

# TODO: add tests for
#   TTYD
#   nullptr
#   All data types
#   All opcodes?

