Despription:
-
This module activates the RTC GPIO (GPIO 0 to 5) as wakeup source for deepsleep for ESP32-C3 modules!




## Import and create module:
```python
    import deepsleep_240723 as deep
```

## Methods
**Restore a rtc buffer:**
```python
    deep.Set_wakeup_pin(pin_nr, **mode=wakeup type, **pull=pull resistances)
 ```
|Parameter|Description|
|-|-|
|pin_nr|GPIO number (0,1,2,3,4,5)|
|mode=0| disable wakeup by RTC GPIO|
|mode=1| wake up the chip upon the rising edge|
|mode=2| wake up the chip upon the failing edge|
|mode=3| wake up the chip upon the rising edge or the failing edge|
|mode=4| wake up the chip upon low level|
|mode=5| wake up the chip upon high level|
|pull=deep.PULL_UP|Pull-up enable of the pin during sleep mode|
|pull=deep.PULL_DOWN|Pull-down enable of pin during sleep mode|
|pull=None|Disable Pull-down and Pull-up|





---
**Create a new rtc buffer:**
```python
    rtcBuffer.Create_new_buffer(data_bit_len=8, header_byte_len=0)
```

**Set value at current pointer:**
```python
    rtcBuffer.Set_value(value, inc=True)
```
Set pointer to given value and increase pointer when inc=True

**Get value from current or arbitrary pointer:**
```python
    rtcBuffer.Get_value(ptr=None)
```
Get last written value (at prevoius pointer position) when ptr is None

**Set header:**
```python
    rtcBuffer.Set_header(value)
```
Value can be *integer* or *bytearray*

**Get header:**
```python
    header = rtcBuffer.Get_header(typ=None)
```
*header* is bytearry if type is None and *integer* if type is 'int' 

**Set pointer:**
```python
    rtcBuffer.Set_ptr(ptr=None)
```
Set pointer and overflow to 0 if ptr is 0 else to the given value 

**Get pointer:**
```python
    pointer,overflow =  rtcBuffer.Get_ptr()
Returns a tuple of pointer and overflow flag
```

---

## Attributes
|Parameter|Description|
|-|-|
|header_byte_len|number of *bytes* for storing the header|
|ptr|Pointer to the **NEXT FREE** element|
|ptr_overflow|Ring buffer is full; pointer starts again from beginning|
|ptr_bit_len|number of *bits*  for storing the pointer|
|ptr_start_bit|bit position where the pointer value is stored|
|ptr_max|*maximum* number of storable values|
|data_bit_len|number *bits* for storing the pointer|
|data_start_bit|bit position where the data are stored|

