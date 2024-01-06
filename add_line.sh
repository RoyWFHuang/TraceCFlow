

#!/bin/bash
function gcc()
{
    /usr/bin/gcc -g -S $@
    cp *.s ./bksfile/
    python3 add_line.py
    /usr/bin/gcc *.s -o out
}

export -f gcc