import re
import os

def parse_header():
    header_files = []
    functions = {}
    includes = []
    for file in os.listdir(os.getcwd()):
        if file.endswith(".h"):
            header_files.append(os.path.join(os.getcwd(), file))
    for file in header_files:
        with open(file, 'r') as f:
            for line in f:
                if re.search(r"^[^{}]*;\s*$", line):
                    if re.search(r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)(?:\s*\**)\s+", line): # get function return type
                        rtv_type = re.search(r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)(?:\s*\**)\s+", line).group().replace(" ", "")
                        print(rtv_type)
                    if re.search(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", line): # get function name
                        function_name = re.search(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", line).group().replace(" ", "").replace("(", "")
                        print(function_name)
                    if re.search(r"\w+(?:\s*\**)(?=\s*\w+\s*(?:,|\)))", line): # get function parameter types
                        param_types_temp = re.findall(r"\w+(?:\s*\**)(?=\s*\w+\s*(?:,|\)))", line)
                        param_types = []
                        for i in param_types_temp:
                            param_types.append(i.replace(" ", ""))
                        print(param_types)
                    functions[function_name] = [function_name, rtv_type, param_types]
    return functions
def parse_c():
    c_files = []
    includes = []
    for file in os.listdir(os.getcwd()):
        if file.endswith(".c"):
            c_files.append(os.path.join(os.getcwd(), file))
    for file in c_files:
        with open(file, 'r') as f:
            for line in f:
                if re.search(r"^#include\s*(.+)", line): # get include statements
                    print("Include: " + re.search(r"^#include\s*(.+)", line).group(1))   
                    includes.append(re.search(r"^#include\s*(.+)", line).group(1))
    return includes
def write_fuzzer(function, includes):
    os.makedirs("fuzzer", exist_ok=True)
    with open(f"fuzzer/{function[0]}_fuzzer.c", 'w') as f:
        for include in includes:
            f.write(f"#include {include}\n")
        f.write("int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {\n")
        f.write(f"    {function[1]} rtv;\n")
        f.write(f"    return 0;\n")
        f.write("}\n")
if __name__ == "__main__":
    functions = parse_header()
    includes = parse_c()
    for name in functions.keys():
        write_fuzzer(functions[name], includes)

# handle only native c data types for now
# fill them with data from the fuzzer