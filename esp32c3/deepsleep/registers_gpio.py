
GPIO_BASE              = const(0x6000_4000)
GPIO_OUT               = const(GPIO_BASE + 0x0004) # Register 5.2. GPIO_OUT values
GPIO_OUT_W1TS          = const(GPIO_BASE + 0x0008) # Register 5.3. set out to high
GPIO_OUT_W1TC          = const(GPIO_BASE + 0x000c) # Register 5.4. set out to low
GPIO_ENABLE            = const(GPIO_BASE + 0x0020) # Register 5.5. overview if gpio is IN or OUT
GPIO_ENABLE_W1TS       = const(GPIO_BASE + 0x0024) # Register 5.6. set gpio to OUT
GPIO_ENABLE_W1TC       = const(GPIO_BASE + 0x0028) # Register 5.7. set gpio to IN
GPIO_STRAP             = const(GPIO_BASE + 0x0038) # Register 5.8. GPIO strapping values
GPIO_IN                = const(GPIO_BASE + 0x003c) # Register 5.9. GPIO_IN values
GPIO_PINn              = const(GPIO_BASE + 0x0074) # Register 5.14.
GPIO_FUNCn_IN_SEL_CFG  = const(GPIO_BASE + 0x0154) # Register 5.16. 0..127 
GPIO_FUNCn_OUT_SEL_CFG = const(GPIO_BASE + 0x0554) # Register 5.18. 0-21 for each GPIO
GPIO_DATE              = const(GPIO_BASE + 0x06FC) # Register 5.19. Version control register (0x2006130)


IOMUX_BASE             = const(0x6000_9000)
IO_MUX_GPIOn           = const(IOMUX_BASE + 0x0004) # Register 5.21. 
IO_MUX_DATE            = const(IOMUX_BASE + 0x00FC) # Register 5.22.  Version control register (0x2006050)

