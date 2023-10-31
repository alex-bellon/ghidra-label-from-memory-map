# Label symbols based on memory map
#
# @author balex
# @category Embedded

from ghidra.program.flatapi import FlatProgramAPI
from cmsis_svd.parser import SVDParser

SVD_DATA_DIR = "."
parser = SVDParser.for_packaged_svd("STMicro", "STM32F103xx.svd")

program = getCurrentProgram()
fpapi = FlatProgramAPI(program)

memory_map = dict()
 
for per in parser.get_device().peripherals:
    per_name = per.name
    per_base = per.base_address
    
    for reg in per.registers:
        reg_name = "mmio:" + per_name + ":" + reg.name
        reg_addr = per_base + reg.address_offset

        for off in range(reg.size//8):

            addr_ = reg_addr + off

            addr = addr_.to_bytes(4, byteorder='little')
            addr ="{}".format(''.join('\\x{:02x}'.format(b) for b in addr))

            memory_map[reg_name + "+" + str(off)] = addr

total = 0

for label in memory_map:

    addr = memory_map[label]
    results = fpapi.findBytes(None, addr, 500)

    for r in results:
        fpapi.createLabel(r, label, True)

    total += len(results)

    print("Created {} labels for {} ({})".format(len(results), label, addr))

print("Creates {} labels total".format(total))
