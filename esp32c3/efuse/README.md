
Despription:
-
This module read and manupulate the ESP32C3 EFUSE registers:

 - The EFUSE memory contains of 11 Blocks (BLOCK0 - BLOCK10), where BLOCK0 and BLOCK1 are 6 registers long (6x32bit)  and BLOCK2~BLOCK10 are 8 registers long (8x32 bit)
 - A BLOCK registers can not read/write directly
 - A *read* command reads ALL BLOCK *at once* into the corresponding DATA READ REGISTERS. These are RO(!)
 - A *programming* command copies the content of the PGM_DATA registers back the registers of thhe desired BLOCK (0-10)
 - A RS(44,32) check confirms the integrity of the PGM data

## Import and create module:
```python
    import efuse_240725 as __efuse
    efuse = __efuse.EFUSE()
```

## Methods for READing

**Read ALL BLOCKS:**
```python
    efuse.Read_blocks()
```
read ALL blocks at once into the corresonding DATA READ REGISTERS.

**Get one block:**
```python
    efuse.Copy_block(block_nr)
```
copy a specific block from *block_nr* to PGM_DATA registers.

**Print the content of the PGM Data Registers:**
```python
    efuse.Print_PGM_DATA()
```
Print the content of the 8 PGM_DATA and 3 PGM_CHECK registers.

**Print the content of the Block Data Registers:**
```python
    efuse.Print_block(block_nr)
```
Print the content of the Block data register.


## Methods for manipulating registers

**Get value of PGM_DATA register:**
```python
    reg_value = efuse.Get_PGM_DATA_register(reg_nr)
```
return the value of the PGM_DATA[*data_nr*]; data_nr=0~7.

**Set value of PGM_DATA register:**
```python
    efuse.Set_PGM_DATA_register(reg_nr, value)
```
set value of the PGM_DATA[*data_nr*]; data_nr=0~7.


**Set all PGM_DATA registers to 0:**
```python
    efuse.Clr_PGM_DATA()
```

## Methods for progarmming (writing) register

**copy content of PGM_DATA registers to corresponding BLOCK registers:**
```python
    efuse.Programm_block(block_nr)
```
block_nr=0~10.

**calculates the RS(44,32) values of the 8 PGM_DATA registers and write the resuslt into 3 PGM_CHECK registers:**
```python
    efuse.Set_PGM_CHECK()
```

**print content of REPORT REGISTERS to indicate an error:**
```python
    efuse.Print_Report()
```



