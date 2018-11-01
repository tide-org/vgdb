import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ptyprocessdir = os.path.join(currentdir, "lib/ptyprocess")
pexpectdir = os.path.join(currentdir, "lib/pexpect")
sys.path.insert(0, ptyprocessdir)
sys.path.insert(0, pexpectdir)

import pexpect
import vim


def start_gdb(commands):
    try:
        print("starting gdb with commands: " + commands)
        child = pexpect.spawnu('/usr/bin/env gdb --interpreter=mi2 ls')
        child.expect('\(gdb\)')
        child.sendline('info')
        child.expect('\(gdb\)')
        print("here1")
        vim.command("let g:test = ''")
        lines = child.before.replace("\r","").split("\n")
        for line in lines:
            print(line)
            vim.command("let g:test = g:test . '" + line + "'")
        print("here2")
    except Exception as ex:
        print("error in python: " + ex)


