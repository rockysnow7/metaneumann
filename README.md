# metaneumann
This is an emulator of a (/inspired by) Von Neumann computer with its own assembly language which can be used to program it. The contents of all registers, RAM, and the hard drive can be viewed while any assembly language programs run in the "debug view".
It was written in Python.


## The Language
* **nop** - no operation
* **out** - output the contents of Register A
* **hlt** - stop the program
* **lha** - load the contents of HDD at address (addr) into Register A
* **lra** - load the contents of RAM at address (addr) into Register A
* **svr** - save the contents of Register A into RAM at address (addr)
* **add** - set Register A to the sum of the contents of Register A and RAM at address (addr)
* **sub** - set Register A to the difference between the contents of Register A and RAM at address (addr)
* **jmp** - set PC to the contents of RAM at address (addr)
* **jmc** - set PC to the contents of RAM at address (addr) if the Carry Flag has been set

All commands require an argument of a denary number from 0-15 (4-bit binary), which is always an address.
The top three commands, "nop", "out", and "hlt" need an argument, but it is not used and is therefore irrelevant (i.e. you can give any number 0-15 and it will have no effect).

**Note: programs can have a maximum 16 lines, due to the size-limitation of each command (I am working on this)**
