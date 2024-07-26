from machine import mem32 as __mem32
from utime import sleep_ms as __sleep_ms; from utime import ticks_us as __ticks; from utime import ticks_diff as __ticks_diff

from . import rs4432 as __rs4432

EFUSE_BASE 					= const(0x6000_8800)
PGM_DATA_REGISTER			= const(EFUSE_BASE + 0x0000) # n=0..7 registers with data to be programmed
PGM_CHECK_REGISTER			= const(EFUSE_BASE + 0x0020) # RS code
READ_DATA_REGISTER			= const(EFUSE_BASE + 0x002c) # register with dada blocks (RO)
EFUSE_PGM_CHECK_VALUE		= const(EFUSE_BASE + 0x002c) # n=0..2 registers with RS code to be programmed.
EFUSE_BLOCK_BASE			= const(EFUSE_BASE + 0x002c) # Base register of 
EFUSE_RD_WR_DIS         	= const(EFUSE_BASE + 0x002c) # reg 4.12: programming of eFuse part is disabled (1) or enabled(0) 
EFUSE_RD_REPEAT_DATAn		= const(EFUSE_BASE + 0x0030) # n=0..4 REPEAT data registers (RO)
EFUSE_RD_MAC_SPI_SYS_n		= const(EFUSE_BASE + 0x0044) # n=0..4
EFUSE_RD_SYS_PART1_DATAn	= const(EFUSE_BASE + 0x005c) # Reg 4.24

EFUSE_RD_REPEAT_ERRn 		= const(EFUSE_BASE + 0x017c)
EFUSE_RD_RS_ERRn			= const(EFUSE_BASE + 0x01C0)

EFUSE_CONF					= const(EFUSE_BASE + 0x01CC) # Register 4.104. Operate programming command 0x5AA5: Operate read command.
EFUSE_CMD					= const(EFUSE_BASE + 0x01D4) # Register 4.105
EFUSE_INT_ST				= const(EFUSE_BASE + 0x01DC) # 4.112.
EFUSE_INT_ENA				= const(EFUSE_BASE + 0x01E0) # 4.113
EFUSE_INT_CLR				= const(EFUSE_BASE + 0x01E4) # 4.114.
EFUSE_DATE					= const(EFUSE_BASE + 0x01FC) # Register 4.115: 0x2006300
#XX = const(BASE +)

CMD_READ 		= const(0x5aa5)
CMD_PROGRAMMING	= const(0x5a5a)

__BLOCK_LEN = (6,6,8,8,8,8,8,8,8,8,8)


class EFUSE(__rs4432.RS):
    def __init__(self):
        super().__init__()
        block = 0
    
    def Register(self, addr, pos, length, val = None):
        ''' set and get register '''
        reg_val = __mem32[addr]
        if val == None:
            ''' GET "value" with "bit_length" at "postition" of "register_value" '''
            pattern = (1<<length) - 1
            return (reg_val >> pos) & pattern
        else:
            ''' SET "value_to_set" at "postition" with "bit_length" into "register_value" '''
            val &= ((1<<length) - 1)
            lsb_val = reg_val & ((1<<pos) - 1)
            shift = pos + length
            msb_val = (reg_val >> shift) << shift
            new_reg_val = msb_val | (val << pos) | lsb_val
            __mem32[addr] = new_reg_val
            return new_reg_val

    def Register_print(self, reg, sep='-', every=8):
        ''' Print a register as binary with seperators '''
        s = f'{self.Register(reg, 0, 32):032b}'
        return sep.join(s[i:i+every] for i in range(0, len(s), every))
    
    # 1 READ BLOCKS
    # 1.1
    def Read_blocks(self):
        ''' Read ALL bloack at once into  DATA READ REGISTERS '''
        # Read blocks
        self.Register(EFUSE_CONF, 0, 1, CMD_READ)  # Set read command
        self.Register(EFUSE_CMD, 0, 1, 1)          # send read command
        while self.Register(EFUSE_CMD, 0, 1):
            '''  check read_done interrupt '''
            __sleep_ms(10)
    
    # 1.2
    def Copy_block(self, block_nr=11):
        ''' Copy block from DATA_READ REGISTER to PGM_DATA registers '''
        assert block_nr<=10, 'Block number (0~10) needed!'
        self.Clr_PGM_DATA_registers()
        block_base_addr = READ_DATA_REGISTER + 4*(sum(__BLOCK_LEN[:block_nr]))
        # Print blocks
        for i in range(__BLOCK_LEN[block_nr]):
            addr_block = block_base_addr + (i<<2)
            addr_pgm  =  PGM_DATA_REGISTER + (i<<2)
            __mem32[addr_pgm] = __mem32[addr_block]
            #print(f'{i} Reg_0x{addr:04x}: 0x{self.Register(addr, 0, 32):08x} {self.Register_print(addr)}')
        print(f'BLOCK {block_nr} copied to PGM_DATA')
    
    # 1.3
    def Print_block(self, block_nr=11):
        assert block_nr<=10, 'block number max 10!'
        ''' Print DATA_READ REGISTER '''
        block_base_addr = READ_DATA_REGISTER + 4*(sum(__BLOCK_LEN[:block_nr]))
        print(f'BLOCK {block_nr} starting at 0x{block_base_addr:08x}:')
        for i in range(__BLOCK_LEN[block_nr]):
            addr_block = block_base_addr + (i<<2)
            print(f'{i} Reg_0x{addr_block:04x}: 0x{self.Register(addr_block, 0, 32):08x} {self.Register_print(addr_block)}')
    
    # 1.4
    def Print_PGM_DATA_registers(self):
        print(f'PGM_DATA registers:')
        for i in range(8):
            addr_pgm = PGM_DATA_REGISTER + (i<<2)
            print(f'{i} Reg_0x{addr_pgm:04x}:  0x{self.Register(addr_pgm, 0, 32):08x} {self.Register_print(addr_pgm)}')
        print(f'PGM_CHECK registers:')
        for i in range(3):
            addr_chk = PGM_CHECK_REGISTER + (i<<2)
            print(f'{i} Reg_0x{addr_chk:04x}:  0x{self.Register(addr_chk, 0, 32):08x} {self.Register_print(addr_chk)}')
    
    # 2: Manipulating PGM_DATA
    # 2.1
    def Set_PGM_DATA_register(self, reg_nr, val):
        assert reg_nr<=7, 'Wrong register number!'
        __mem32[PGM_DATA_REGISTER + (reg_nr<<2)] = val & 0xffff_ffff
        self.Set_PGM_CHECK()
    
    # 2.2
    def Get_PGM_DATA_register(self, reg_nr=10):
        assert reg_nr<=7, 'Wrong or no register number!'
        return __mem32[PGM_DATA_REGISTER + (reg_nr<<2)]
      
    # 2.3 
    def Clr_PGM_DATA_registers(self):
        ''' Clear PGM_DATA '''
        print(f'Clear PGM_DATA')
        for i in range(11):
            __mem32[PGM_DATA_REGISTER + (i<<2)] = 0
            
    # 3 PROGRAMM BLOCK
    # 3.1
    def Programm_block(self, block_nr=11):
        ''' copy block to PGM_DAT '''
        assert block_nr<=10, 'block number max 10!'
        self.Register(EFUSE_CMD, 2, 4, block_nr)   # Set EFUSE_BLK_NUM to block number
        self.Set_PGM_CHECK() 
        self.Register(EFUSE_CONF, 0, 16, CMD_PROGRAMMING) # Command programming
        self.Register(EFUSE_CMD, 1, 1, 1)          # send programming command
        while self.Register(EFUSE_CMD, 0, 1):
            '''  check read_done interrupt '''
            __sleep_ms(10)
        self.Clr_PGM_DATA()
        print(f'Block {block_nr} programmed!')
    
    # 3.2 RS(44,32 check):
    def Set_PGM_CHECK(self):
        ''' set the PGM_CHECK_REGISTER acconding to PGM_DATA data '''
        data = 32*[0]
        k = 0
        for i in range(8):
            addr_pgm = PGM_DATA_REGISTER + (i<<2)
            for j in range(3, -1, -1):
                data[k] = self.Register(addr_pgm, j<<3, 8)
                k += 1
        check = self.Encode_msg(data)[32:]
        for i in range(3):
            addr = PGM_CHECK_REGISTER + (i<<2)
            value = 0
            for j in range(4):
                pos = 4*i + j
                shift = (3-j)<<3
                value += (check[pos]<<shift)
            __mem32[addr] = value
    
    # 3.3 
    def Print_Report(self):
        ''' did an error occured? '''
        print('ERROR codes')
        for i in range(5):
            addr = EFUSE_RD_REPEAT_ERRn + (i<<2)
            print(f'BLOCK0    at 0x{addr:04x}: 0x{self.Register(addr, 0, 32):08x} - b{self.Register_print(addr)}', end=' ')
            print('OK') if not __mem32[addr] else print('error')
        for i in range(2):
            addr = EFUSE_RD_RS_ERRn + (i<<2)
            print(f'BLOCK1-10 at 0x{addr:04x}: 0x{self.Register(addr, 0, 32):08x} - b{self.Register_print(addr)}', end=' ')
            print('OK') if not __mem32[addr] else print('error')


