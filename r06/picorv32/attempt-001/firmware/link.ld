ENTRY(_start)
SECTIONS { . = 0; .text : { *(.text.start) *(.text*) } .rodata : { *(.rodata*) } .data : { *(.data*) *(.sdata*) } PROVIDE(__global_pointer$ = . + 0x800); .bss : { *(.bss*) *(.sbss*) *(COMMON) } /DISCARD/ : { *(.comment) *(.riscv.attributes) *(.eh_frame*) } }
