from machine import mem32 as __mem32
from utime import sleep_ms as __sleep_ms
from math import log2 as __lg
from .registers_rtc import *
from .registers_gpio import *

VERBOSE   = False
PULL_DOWN = 1
PULL_UP   = 2



def Register(addr, pos, length, val = None):
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


def Print_register(reg, sep='-', every=8):
    ''' Print a register as binary with seperators '''
    s = f'{Register(reg, 0, 32):032b}'
    return sep.join(s[i:i+every] for i in range(0, len(s), every))

def __reset_wakeup_pin():
    active_pins = Register(RTC_CNTL_GPIO_WAKEUP, 26, 6)
    if not active_pins:
        return
    Register(RTC_CNTL_GPIO_WAKEUP, 6, 1, 1) # Clear the RTC GPIO wakeup flag --> clears RTC_CNTL_GPIO_WAKEUP_STATUS
    Register(RTC_CNTL_GPIO_WAKEUP, 6, 1, 0) # Set bit to 0 again
    for i in range(6):
        if not active_pins&(1<<i):
            continue
        pin_nr = 5 - i
        addr = IO_MUX_GPIOn + (pin_nr<<2)
        Register(addr, 4, 1, 1) # set MCU_IE
        print(f'IO_MUX_GPIO_{pin_nr} {'':>6} at 0x{addr:08x} {Print_register(addr)[18:]:>35}') if VERBOSE else None

def __set_thres(ds_time_s):
    # 1. get current tick value
    Register(RTC_CNTL_TIME_UPDATE, 31, 1, 1) # 9-4: RTC_CNTL_TIME_UPDATE: Selects the triggering condition for the RTC timer
    t_now = Register(RTC_CNTL_TIME_LOW0, 0, 32) + (Register(RTC_CNTL_TIME_HIGH0, 0, 16) << 32)
    print('Current RTC_SLOW TICKS', t_now, '\r\n') if VERBOSE else None
    # 2. set threshold
    t_thres = int(t_now + ds_time_s * 136_000) # 1 seconds
    Register(RTC_CNTL_SLP_TIMER0, 0, 32, t_thres)
    Register(RTC_CNTL_SLP_TIMER1, 0, 16, t_thres>>32)
    Register(RTC_CNTL_SLP_TIMER1, 16, 1, 1) #  RTC_CNTL_MAIN_TIMER_ALARM_EN
    #Register(RTC_CNTL_TIME_UPDATE, 31, 1, 1) # 9-4: RTC_CNTL_TIME_UPDATE: Selects the triggering condition for the RTC timer
    
def __triggers(a=0, b=0, c=0):
    ''' set Register 9.4. Selects the triggering condition for the RTC timer '''
    Register(RTC_CNTL_TIME_UPDATE, 27, 1, a) # TIMER_SYS_STALL Selects the triggering condition for the RTC timer
    Register(RTC_CNTL_TIME_UPDATE, 28, 1, b) # TIMER_XTL_OFF Selects the triggering condition for the RTC timer
    Register(RTC_CNTL_TIME_UPDATE, 29, 1, c) # TIMER_SYS_RST Selects the triggering condition for the RTC timer

def __cpu_stalling(val=0):
    ''' set Register 9.8. '''
    Register(RTC_CNTL_TIMER1, 6, 8, 0x10) # RTC_CNTL_FOSC_WAIT Sets the FOSC clock waiting cycles (using the RTC slow clock)
    Register(RTC_CNTL_TIMER1, 24, 8 , 40) # RTC_CNTL_PLL_BUF_WAIT Sets the PLL waiting cycles (using the RTC slow clock)
    Register(RTC_CNTL_TIMER2, 24, 8 , 1) #  minimal cycles for FOSC clock (using the RTC slow clock) when powered down
    Register(RTC_CNTL_TIMER5, 8, 8 , 0x80) #  minimal sleep cycles (using the RTC slow clock)
    if val:
        Register(RTC_CNTL_TIMER1, 0, 1, 1) # enable cpu stalling
        Register(RTC_CNTL_SW_CPU_STALL, 26, 8 , 0x21) #RTC_CNTL_SW_STALL_PROCPU_C1 = 0x21
        Register(RTC_CNTL_OPTIONS0, 2, 2, 0x2) # RTC_CNTL_SW_STALL_PROCPU_C0 = 2
    else:
        Register(RTC_CNTL_TIMER1, 0, 1, 0) # enable cpu stalling
        Register(RTC_CNTL_SW_CPU_STALL, 26, 8 , 0) #RTC_CNTL_SW_STALL_PROCPU_C1 = 0x21
        Register(RTC_CNTL_OPTIONS0, 2, 2, 0) # RTC_CNTL_SW_STALL_PROCPU_C0 = 2

def Deepsleep(ds_time_s):
    __set_thres(ds_time_s)
    __cpu_stalling(0)
    __triggers(0,0,0)
    __reset_wakeup_pin()
    Register(RTC_CNTL_RESET_STATE, 16, 1, 1) # RTC_CNTL_ALL_RESET_FLAG_CLR_PROCPU Clears the CPU reset flag.
    Register(RTC_CNTL_RESET_STATE, 13, 1, 1) # RTC_CNTL_STAT_VECTOR_SEL_PROCPU:  Selects the CPU static vector
    Register(RTC_CNTL_WAKEUP_STATE, 15, 17, 0x1000 + 0x8 + 0x4) # Selects the wakeup source acc tab 9-4
    Register(RTC_CNTL_INT_ENA_RTC, 10, 1, 0) # Enables the RTC timer interrupt
    Register(RTC_CNTL_STATE0, 29, 1, 1) # Sleep wakeup bit.
    __sleep_ms(10) if VERBOSE else None
    Register(RTC_CNTL_STATE0, 31, 1, 1) # Sends the chip to sleep.

def Set_wakeup_pin(pin_nr=None, **kwargs):
    ''' Set wake up pin; in pin_nr is None, all wakeup pins are deleted'''
    if pin_nr is None:
        Register(RTC_CNTL_GPIO_WAKEUP, 26, 6, 0)
        return 
    assert pin_nr<=5, 'RTC GPIO needed!'
    mode = kwargs['mode'] if 'mode' in kwargs else 3
    pull = kwargs['pull'] if 'pull' in kwargs else 0
    
    # 1 set GPIO registers
    Register(GPIO_ENABLE_W1TC, pin_nr, 1, 1) # set pin as IN
    print(f'GPIO_ENABLE {'':>8} at 0x{GPIO_ENABLE:08x} {Print_register(GPIO_ENABLE)[22:]:>35}') if VERBOSE else None
    print(f'GPIO_IN {'':>12} at 0x{GPIO_IN:08x} {Print_register(GPIO_IN)[22:]:>35}') if VERBOSE else None
    
    # 2 set IOMUX registers
    addr = IO_MUX_GPIOn + (pin_nr<<2)
    Register(addr, 1, 1, 1) # set SLP_SEL
    Register(addr, 2, 1, 0) # MCU_WPD
    Register(addr, 3, 1, 0) # MCU_WPU
    if pull is PULL_DOWN:
        Register(addr, 2, 1, 1) # MCU_WPD
    elif pull is PULL_UP:
        Register(addr, 3, 1, 1) # MCU_WPD
    Register(addr, 4, 1, 1) # set MCU_IE
    print(f'IO_MUX_GPIO_{pin_nr} {'':>6} at 0x{addr:08x} {Print_register(addr)[18:]:>35}') if VERBOSE else None
    
    # 3 set RTC_CNTL_GPIO_WAKEUP
    Register(RTC_CNTL_GPIO_WAKEUP, 23 - 3*pin_nr, 3, mode) # RTC_CNTL_GPIO_PINn_INT_TYPE: Configures RTC GPIO n wakeup type
    Register(RTC_CNTL_GPIO_WAKEUP, 31 - pin_nr, 1, 1)      # RTC_CNTL_GPIO_PINn_WAKEUP_ENABLE: Enables wakeup from RTC GPIO 5
    Register(RTC_CNTL_GPIO_WAKEUP, 7, 1, 1) # RTC_CNTL_GPIO_PIN_CLK_GATE Enables the RTC GPIO clock gate
    print(f'RTC_CNTL_GPIO_WAKEUP at 0x{RTC_CNTL_GPIO_WAKEUP:08x} {Print_register(RTC_CNTL_GPIO_WAKEUP)}') if VERBOSE else None
    # 4
    #Register(RTC_CNTL_GPIO_WAKEUP, 6, 1, 1) # Clear the RTC GPIO wakeup flag --> clears RTC_CNTL_GPIO_WAKEUP_STATUS
    #Register(RTC_CNTL_GPIO_WAKEUP, 6, 1, 0) # Set bit to 0 again

   
def Get_reservation_registers():
    ''' Returns the 8 reservation registers '''
    reg_prop = ['Res', 'RTC_SLOW_CLK calibration value', 'Boot time low word', 'Boot time high word', 'External XTAL frequency',
                'APB bus frequency', 'FAST_RTC_MEMORY_ENTRY', 'FAST_RTC_MEMORY_CRC']
    for i in range(8):
        addr = RTC_CNTL_STORE0 + (i<<2) if i<4 else RTC_CNTL_STORE4 + ((i-4)<<2)
        print(f'Reg{i} at at 0x{addr:08X}: {__mem32[addr]&0xffff_ffff:>10d} ({reg_prop[i]})')

def Get_reset_cause():
    ''' Returns reset cause based on table '''
    return Register(RTC_CNTL_RESET_STATE, 0, 6)

def Get_wakeup_pin():
    ''' return pin number that interrupted the deepsleep or None if there was not GPIO event '''
    reg =  Register(RTC_CNTL_GPIO_WAKEUP, 0, 6)
    try:
        return int(__lg(reg)//__lg(2))
    except ValueError:
        return None

def Get_wakeup_cause():
    ''' return 0x8 if deepsleep ended by timer interrupt or 0x4 if ended by gpio interrupt --> Table 9-4. '''
    return Register(RTC_CNTL_SLP_WAKEUP_CAUSE, 0, 17)
