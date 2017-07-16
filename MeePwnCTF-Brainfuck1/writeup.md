# Brainfuck1
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled

This program converts brainfuck into x86.

In the main function a BrainfuckVM object is allocated, which has the following members:

BrainfuckVM {
 QWORD PTR array
 QWORD PTR jitbuffer_base
 QWORD array_size
 QWORD jitbuffer_idx
 QWORD jitbuffer_size
}

The key observations to solve this challenge are:
- The jitbuffer remains writeable, so we can place shellcode in the jitbuffer.
- The array is allocated on the heap, right after the BrainfuckVM object.
- There is no bounds checking on the array, so we can move the pointer outside the array bounds.

In order to solve the challenge, we can do the following:
 - Leak the jitbuffer address.
 - Overwrite the array address in the BrainfuckVM object with the jitbuffer address.
 - Write our shellcode in the jitbuffer to spawn a shell.