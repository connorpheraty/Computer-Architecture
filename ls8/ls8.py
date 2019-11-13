#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()


cpu.add_instructions()
cpu.load()

#cpu.ram_read()

cpu.run()