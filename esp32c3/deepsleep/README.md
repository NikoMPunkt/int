Despription:
-
This module activates the RTC GPIO (GPIO 0 to 5) as wakeup source for deepsleep for ESP32-C3 modules!




## Import and create module:
```python
    import deepsleep_240723 as deep
```

## Methods
**Set RTC GPIO pin as wakeup source:**
```python
    deep.Set_wakeup_pin(pin_nr, **mode=wakeup type, **pull=pull resistances)
 ```
|Parameter|Description|
|-|-|
|pin_nr|GPIO number (0,1,2,3,4,5)|
|mode=0| disable wakeup by RTC GPIO|
|mode=1| wake up upon rising edge|
|mode=2| wake up chip upon falling edge|
|mode=3| wake up chip upon rising or falling edge|
|mode=4| wake up chip upon low level|
|mode=5| wake up chip upon high level|
|pull=deep.PULL_UP|Pull-up enable of pin during sleep mode|
|pull=deep.PULL_DOWN|Pull-down enable of during sleep mode|
|pull=None|Disable Pull-down and Pull-up|

---
**Set CPU into deepsleep:**
```python
    deep.Deepsleep(ds_time)
```
ds_time in seconds!

**Get reset cause:**
```python
    reset_cause = deep.Get_reset_cause()
```
Return the reset cause 

**Get wakeup cause:**
```python
    wakeup_cause = deep.Get_wakeup_cause()
```
|wakeup_cause|Description|
|-|-|
|0x04|wakeup by GPIO event|
|0x08|wakeup by timer|

**Get pin wakeup:**
```python
    wakeup_pin = deep.Get_wakeup_pin()
```
return the GPIO pin number which caused the wakeup event or None when timer caused the evenet



