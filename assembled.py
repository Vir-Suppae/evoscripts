import sys
import re

def sanitize(code: str) -> str:
    code = re.sub(r"\s",'',code)
    code = re.sub(r";.*?;", '', code)
    if len(code) % 2 != 0:
        raise SyntaxError("instruction missing argument")
    return code

def interpret(code: str, MAX_LENGTH: int) -> dict[str, int]:
    registers = {char: 0 for char in "0123456789ABCDEFGHIJKLMNOPQRSTUV"}
    code = sanitize(code)

    paired_code = list(zip(code[::2], code[1::2]))

    pc = 0

    step = 0
    while 0 <= pc < len(paired_code) and step < MAX_LENGTH:
        match paired_code[pc]:
            case ("/", "/"):
                break
            case ("+", r) if registers.get(r) is not None:
                registers[r] += 1
                pc += 1
            case ("-", r) if registers.get(r) is not None:
                registers[r] -= 1
                pc += 1
            case (">", r) if registers.get(r) is not None:
                sys.stdout.buffer.write(bytes((registers[r] % 256,)))
                pc += 1
            case ("<", r) if registers.get(r) is not None:
                byte = sys.stdin.buffer.read(1)
                registers[r] = byte[0] if byte else registers[r]
                pc += 1
            case ("m", r) if registers.get(r) is not None:
                pc += registers[r]
            case ("l", r) if registers.get(r) is not None:
                pc = registers[r]
            case (a, b) if registers.get(a) is not None and registers.get(b) is not None:
                if registers[a] != registers[b]:
                    pc += 1
                pc += 1
            case _:
                raise NotImplementedError
        step += 1

    return registers
