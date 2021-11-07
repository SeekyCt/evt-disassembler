# Opcode Namer: handles instruction names

class OpcodeNamer:
    def __init__(self, spm: bool, cpp_macros: bool):
        # Base list, starting from 1
        opcodes = [
            "end_script", "end_evt", "lbl", "goto", "do", "while", "do_break",
            "do_continue", "wait_frm", "wait_msec", "halt", "if_str_equal",
            "if_str_not_equal", "if_str_small", "if_str_large", "if_str_small_equal",
            "if_str_large_equal", "iff_equal", "iff_not_equal", "iff_small",
            "iff_large", "iff_small_equal", "iff_large_equal", "if_equal",
            "if_not_equal", "if_small", "if_large", "if_small_equal", "if_large_equal",
            "if_flag", "if_not_flag", "else", "end_if", "switch", "switchi",
            "case_equal", "case_not_equal", "case_small", "case_large", "case_small_equal",
            "case_large_equal", "case_etc", "case_or", "case_and", "case_flag",
            "case_end", "case_between", "switch_break", "end_switch", "set", "seti",
            "setf", "add", "sub", "mul", "div", "mod", "addf", "subf", "mulf", "divf",
            "set_read", "read", "read2", "read3", "read4", "read_n", "set_readf",
            "readf", "readf2", "readf3", "readf4", "readf_n", "clamp_int", "set_user_wrk",
            "set_user_flg", "alloc_user_wrk", "and", "andi", "or", "ori", "set_frame_from_msec",
            "set_msec_from_frame", "set_ram", "set_ramf", "get_ram", "get_ramf", "setr",
            "setrf", "getr", "getrf", "user_func", "run_evt", "run_evt_id", "run_child_evt",
            "delete_evt", "restart_evt", "set_pri", "set_spd", "set_type", "stop_all",
            "start_all", "stop_other", "start_other", "stop_id", "start_id", "chk_evt",
            "inline_evt", "inline_evt_id", "end_inline", "brother_evt", "brother_evt_id",
            "end_brother", "debug_put_msg", "debug_msg_clear", "debug_put_reg",
            "debug_name", "debug_rem", "debug_bp"
        ]

        # Remove SPM-only opcode for TTYD
        if not spm:
            opcodes.remove("clamp_int") 

        # Build name and opcode dicts
        self.names = {}
        for i, name in enumerate(opcodes):
            opc = i + 1
            self.names[opc] = name
        
        # Store macro flag
        self.cpp_macros = cpp_macros

    # Gets the name for an opcode
    def opc_to_name(self, opc: int) -> str:
        return self.names[opc]

    # Considers macro mode for a name
    def name_to_printing_name(self, name: str) -> str:
        if self.cpp_macros:
            if name == "end_evt":
                return "RETURN"
            elif name == "end_script":
                return "EVT_END"
            else:
                return name.upper()
        else:
            return name
