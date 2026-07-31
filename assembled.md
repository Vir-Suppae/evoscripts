# assembled Specification

## Overview

**assembled** is a minimal interpreted register machine designed for simplicity and mutation-friendly program evolution.

Programs consist of a sequence of fixed-width instructions. Every instruction is exactly **two ASCII characters**, allowing programs to be easily generated, mutated, and parsed.

Execution proceeds sequentially until a halt instruction is encountered, the program counter leaves the program, or an implementation-defined step limit is reached.

---

## Registers

The machine provides **33 registers**.

General-purpose registers:

```
0 1 2 3 4 5 6 7 8 9
A B C D E F G H I J K L M N O P Q R S T U V
```

Additionally, the machine contains a **scratch register**. The scratch register is used by data movement and arithmetic instructions.

All registers store arbitrary signed integers.

Registers are initialized to zero before execution begins.

---

## Program Format

Programs are plain text.

Before execution:

* All whitespace is removed.
* Comments are removed.
* The remaining text is interpreted as a sequence of two-character instructions.

If the remaining source has an odd number of characters, execution fails with a syntax error.

---

## Comments

Comments are delimited by semicolons.

```
; this is a comment ;
```

Comments may contain any text except for semicolons.

---

## Execution Model

Execution begins at instruction index `0`.

The machine maintains:

* a program counter,
* the register file,
* the scratch register,
* an implementation-defined instruction counter.

Instructions execute sequentially unless modified by a jump instruction.

Execution terminates when:

* the `//` instruction is executed,
* the program counter moves outside the program,
* or the implementation-defined instruction limit is reached.

---

## Instruction Set

### Register Operations

`+r`

Increment register `r`.

---

`-r`

Decrement register `r`.

---

`.r`

Set register `r` to zero.

---

### Input and Output

`<r`

Read one byte from standard input into register `r`.

If end-of-file is reached, register `r` is left unchanged.

---

`>r`

Write the low byte of register `r` to standard output.

The emitted byte is:

```
register[r] mod 256
```

---

### Scratch Register

`[r`

Copy register `r` into the scratch register.

---

`]r`

Copy the scratch register into register `r`.

---

### Arithmetic

Arithmetic instructions always modify the scratch register.

`pr`

```
scratch = scratch + register[r]
```

---

`sr`

```
scratch = scratch - register[r]
```

---

`tr`

```
scratch = scratch * register[r]
```

---

`dr`

```
scratch = scratch // register[r]
```

Integer division follows the host language's integer division semantics.

If `register[r]` is zero, the scratch register is left unchanged.

---

### Control Flow

`mr`

Move the program counter relative to its current position by the value stored in register `r`.

---

`lr`

Set the program counter to the value stored in register `r`.

---

`AB`

Compare registers `A` and `B`.

If the two registers are equal, execution proceeds normally.

If they are not equal, the following instruction is skipped.

---

`//`

Terminate execution immediately.

---

## Errors

Execution fails with a syntax error if:

* an instruction uses an invalid register identifier,
* an instruction is undefined,
* or the sanitized source contains an odd number of characters.

---

## Register Identifiers

Valid register identifiers are:

```
0123456789ABCDEFGHIJKLMNOPQRSTUV
```

The scratch register is not directly addressable by source code and may only be accessed through the `[` and `]` instructions and the arithmetic instructions.

---

## Design Goals

assembled is intended to be:

* minimal,
* deterministic,
* easy to interpret,
* easy to mutate by evolutionary algorithms,
* and simple to implement on a wide variety of host systems.

---

## Examples

Hello

```
+0+0+0+0+0+0+0+0[0.0
+0+0+0t0+0+0+0+0+0t0]0 ; 0=H ;
>0
+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1 ; 1=e-H ;
[1 p0 ]0
>0
+2+2+2+2+2+2+2 ; 2=l-e;
[2 p0 ]0
>0>0
+3+3+3
[3 p0 ]0
>0
```
