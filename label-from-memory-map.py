# Label symbols based on memory map
#
# @author balex
# @category Embedded

from ghidra.program.flatapi import FlatProgramAPI
from cmsis_svd.parser import SVDParser

SVD_DATA_DIR = "."
parser = SVDParser.for_packaged_svd("STMicro", "STM32F103xx.svd")

for peripheral in parser.get_device().peripherals:
    print("%s @ 0x%08x" % (peripheral.name, peripheral.base_address))

exit()

program = getCurrentProgram()
fpapi = FlatProgramAPI(program)

memory_map_raw = open("/home/alex/GitHub/ghidra-label-from-memory-map/stm32f103zg", "r").readlines()
memory_map = dict()

for line in memory_map_raw:

    line = line.strip("\n")
    chunks = line.split(" ")
    
    start_ = chunks[0].replace("0x", "") + chunks[1]
    end_ = chunks[3].replace("0x", "") + chunks[4]
    name = '_'.join(chunks[5:])
    
    start = bytearray.fromhex(start_) # ghidra is using python 2
    start.append(b'\\')
    start.reverse()

    end = bytearray.fromhex(end_)
    end.append(b'\\')
    end.reverse()

    memory_map[name] = (start, end)

print(memory_map)

for region in memory_map:

    addr = memory_map[region][0]
    results = fpapi.findBytes(None, str(addr), 500)

    for r in results:
        fpapi.createLabel(r, region, True)

    print("Created {} labels for {}".format(len(results), region))
