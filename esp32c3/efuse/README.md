
Despription:
-
This module read and manupulate the ESP32C3 EFUSE registers:

 - The EFUSE memory contains of 11 Blocks (BLOCK0 - BLOCK10), where BLOCK0 and BLOCK1 are 6 registers long (6x32bit)  and BLOCK2~BLOCK10 are 8 registers long (8x32 bit)
 - A BLOCK registers can not read/write directly but via the 8 scratchpad registers PGM_DATA
 - A *read* command copies the registers content of a specific BLOCK (0-10) into the PGM_DATA registers, which can be manipulated afterwards
 - A *programming* command copies the content of the PGM_DATA registers back the registers of thhe desired BLOCK (0-10)
 - A RS(44,32) check confirms the integrity of the PGM data

## Import and create module:
```python
    import efuse_240725 as __efuse
    efuse = __efuse.EFUSE()
```

## Methods
**Get a BLOCK content**
```python
    efuse.Get_block(block_nr)
```
copy the content of the block *block_nr* into the PGM_DATA registers and print them

---
**Print the content of the PGM Data Registers:**
```python
    efuse.Print_PGM_DATA()
```
return the content of the 8 PGM_DATA and 3 PGM_CHECK registers


**Get value of PGM_DATA register:**
```python
    reg_value = efuse.Get_PGM_DATA(reg_nr)
```
return the value of the PGM_DATA[*data_nr*]; data_nr=0~7

**Set content of PGM_DATA register:**
```python
    efuse.Set_PGM_DATA(reg_nr, value)
```
set value of the PGM_DATA[*data_nr*]; data_nr=0~7

**copy content of PGM_DATA registers to corresponding BLOCK registers**
```python
    efuse.Programm_block(block_nr)
```
block_nr=0~10

**calculates the RS(44,32) values of the 8 PGM_DATA registers and write the resuslt into 3 PGM_CHECK registers**
```python
    efuse.Set_PGM_CHECK()
```

**Set the PGM_DATA registers to 0**
```python
    efuse.Clr_PGM_DATA()
```

**print content of REPORT REGISTERS to indicate an error**
```python
    efuse.Print_Report()
```



