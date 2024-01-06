import os
import glob
import time

TRACE_PRT = f"\n.TRACE_PRT:\n\
    .string    \"%s (%d)\\n\""

def add_trace_num(line_nr, func_lab):
    trace_str = f"\
    movl    ${line_nr}, %edx\n\
    leaq    {func_lab}(%rip), %rax\n\
    movq    %rax, %rsi\n\
    leaq    .TRACE_PRT(%rip), %rax\n\
    movq    %rax, %rdi\n\
    movl    $0, %eax\n\
    call    printf@PLT\n"
    return trace_str


def add_trace_func_lab(func_lab, func_name):
    trace_lab = f"\n{func_lab}:\n\
    .string	\"{func_name}\"\n"
    return trace_lab

path = os.getcwd()
asm_files = glob.glob(os.path.join(path, "*.s"))

for f in asm_files:
    # print("start to read ===============")
    asm_fd = open(f, "r")
    # read the csv file
    asm_code = asm_fd.read()
    # print(asm_code)
    asm_fd.close()

    idx = asm_code.index(".rodata")
    idx = idx + len(".rodata")
    asm_code = asm_code[:idx] + TRACE_PRT + asm_code[idx:]

    # tmp = asm_code
    func_idx_start = 0
    while True:
        try:
            # print(f"start = {func_idx_start}")
            # time.sleep(2)
            func_idx_start = asm_code[func_idx_start:].index(".type") + func_idx_start
            func_idx_start = func_idx_start + len(".type")
            # print(f"after find start = {func_idx_start}")
            func_idx_end = (asm_code[func_idx_start:].index("@function")) + func_idx_start
            func_name = asm_code[func_idx_start:func_idx_end].replace(',', '').replace('\t', '').replace(' ', '')
            func_lab = "." + func_name.upper()
            func_lab_code = add_trace_func_lab(func_lab, func_name)

            asm_code = asm_code[:func_idx_end + len("@function")] + \
                    func_lab_code + asm_code[func_idx_end + len("@function"):]
            func_idx_start = func_idx_end + len("@function")


            func_idx_start = asm_code[func_idx_start:].index(".cfi_startproc") + func_idx_start
            func_idx_end = asm_code[func_idx_start:].index(".cfi_endproc") + func_idx_start

            line_num_start = func_idx_start
            while True:
                try:
                    # print(asm_code[line_num_start:func_idx_end] + "\n")
                    line_num_start = \
                        asm_code[line_num_start:func_idx_end].index(".loc") + len(".loc") + line_num_start
                    line_num_end = \
                        asm_code[line_num_start:func_idx_end].index("\n")+ len("\n") + line_num_start
                    line_num = asm_code[line_num_start:line_num_end].split(" ")[2]
                    # print(f"line num {line_num}")
                    trace_num_code = add_trace_num(line_num, func_lab)
                    asm_code = asm_code[:line_num_end] + trace_num_code + asm_code[line_num_end:]
                    func_idx_end = func_idx_end + len(trace_num_code)
                    line_num_start = line_num_end + len(trace_num_code)
                    # print(f"line_num_start num {line_num_start}/{func_idx_end}")

                except Exception as e:
                    # print(f"error {e}")
                    break


            func_idx_start = func_idx_end
            # print(f"end = {func_idx_start}")
        except Exception as e:
            # print(f"error {e}")
            break

    asm_fd = open(f, "w")
    asm_fd.write(asm_code)
    asm_fd.close()
