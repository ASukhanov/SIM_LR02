# PoF_SIM_L432
Firmware for Nucleo L432KC eval board for SIM_LR02.
Design environment: STM32CubeIDE for Visual Studio Code (2026-05-30)

## Eval Board NUCLEO-L$#!KC, Solder beads
![Top layout](Docs/STM32L432_top_layout.jpg)
![Bottom layout](Docs/STM32L432_bottom_layout.jpg)

SB9 Off to power from +5V<br>
Note: SB16 and SB18 are better be OFF, they connect PA6-PB6 and PA5-PB5.<br>

## Pinout, as defined in firmware/Inc/Board.h
```
//-----------------+-------------------+----------------------------------------
//    Pins          STM32               Arduino
#define LED_GREEN   LED_GREEN_GPIO_Port,LED_GREEN_Pin// PA12
#define LED_RED     LED_RED_GPIO_Port,LED_RED_Pin//  PA7
#define LED_BLUE    LED_BLUE_GPIO_Port,LED_BLUE_Pin//  PA6
#define SIM_A1      A1_GPIO_Port,A1_Pin// PA11 OpAmp gain
#define SIM_A0      A0_GPIO_Port,A0_Pin//  PA8  OpAmp gain
//#define SIM_5V      GPIOC,GPIO_PIN_14// D7  5V_SW. Occupied by RCC_OSC32_OUT
#define SIM_SW_STATE SW_STATE_GPIO_Port,SW_STATE_Pin// PB1
#define SIM_POW_GOOD POW_GOOD_GPIO_Port,POW_GOOD_Pin// PB6
#define SIM_BUSY    BUSY_GPIO_Port,BUSY_Pin//  PB7  Not needed. The Busy state can be determined by bit31 of data.
#define SIM_CS      CS_GPIO_Port,CS_Pin//  PB0
// The following pins are not defined in main.h because they are not used by the main.c directly, but only in board.c. They are defined here to keep all pin definitions in one place.
#define SIM_SCK     GPIOB,GPIO_PIN_3//  PB3 On L432 it is connected to LD3 Green
#define SIM_MISO    GPIOB,GPIO_PIN_4//  PB4
#define SIM_MOSI    GPIOB,GPIO_PIN_5//  PB5
#define SIM_WTX     GPIOA,GPIO_PIN_9//  TX
#define SIM_WRX     GPIOA,GPIO_PIN_10// RX
//-----------------+-------------------+----------------------------------------
Signal 5V_SW is not used on the SIM.
If, by some reason, 5V_SW is active, then following switches required:
SB4-OFF, SB6-ON, SB5-OFF, SB7-OFF, SB8-ON/OFF
```
[Pin Names](Docs/NUCLEO-L432KC_Nano_headersr.png)

[Nano Connector](Docs/NUCLEO-L432KC_Nano_connector.png)

## Power Consumption
Firmware 1.0.6 2026-06-11
LR_02 is set for lowest radio power and fastest data rate: Power=0dBm, Level=7.
The LR_02 supply current is 15 mA. At max power (22dBm) it is 180 mA. 
- Whole board + DX_LR02: **0.25W, 50mA**. 
- Standalone STM32L432, SB9 Off, Power from USB: 0.280W, 54mA
- Standalone STM32L432, SB9 Off, Power from external +5V: 0.060W, 11mA

## Reset
When Reset button is pressed the receiving LR02 unit should receive LORA packet 
with baud rate 115200:
```
Board init. Version 1.0.6. 
```

## Commands
Communication interface: UART1.
All data are ASCII strings.
Format of input commands `<CMD VALUE>`:
List of legal commands:
- `<STS?>`: Request board status:
```
<TSR:0,TO:160,RL:0,T:247993,V:1.0.6>
```
- `<S Value>`: Set sampling rate of the ADC, Value is in range [0:7].
- `<R Value>`: Set recLimit, number of samples to transmit to PIM during each reporting interval.
- `<RI Value>`: Set reporting interval in milliseconds, default 1000.
- `<TO Value>`: Timeout for receiving one character from PIM, it defines data rate.
The actual data delivery interval is the sum of timeout value and the ADC conversion time.
- `<+5V Value>`: Turn On/Off the +5V switch, legal values: 1/0'
- `<DBG Value>`: Debugging control. Bit0: enable output to debugging UART2. Bits1,2 extended debugging. 

## Testing/Debugging
The RS232 with 3.3V levels should be connected: RXD - to PA9 (W_TX), TXD - to PA10 (W_RX).

To communicate with the board over UART1:

    python3 -m serial.tools.miniterm /dev/ttyUSB0 115200

The UART2(over USB) sends debugging information, which is copy of the output sream of UART1

    python3 -m serial.tools.miniterm /dev/ttyACM0 115200

## Data stream from SIM to receiving modem.
The baud rate is the 115200. The max radio bit rate of the LR02 is 13Kbit/s
Reliably it can deliver 50 samples/s.
The standard delivery is statistics over requested period, default 1 s.
The statistics data are ASCII like this:

    <M498,60,-1340092,993,427,1371015>
    <M498,60,-1339997,1134,576,1372158>

Data format of the \<M...> record:<br>
**<Mn1,n2,n3,n4,n5,n6>**. Where n1 is number of samples, received from ADC 
since last report, n2 is number of samples, accumulated for statistics, 
n3: Mean\*10, n4: StDev\*10, n5: peak-to-peak amplitude, n6 clockCounter (1ms)<br>

If enabled, SIM will also deliver samples. For example: 

    <M7,7,-1339327,389,126,1371015><R-133932><R-133936><R-133954><R-133943><R-133980><R-133956><R-133939>
    <M7,7,-1339485,152,48,1372158><R-134004><R-133935><R-133932><R-133982><R-133959><R-133941><R-133932>

Data format (ASCII) of the \<R...> record:<br>
**\<Rn1>**. Where n1 is ADC reading.<br>
Reading 0 corresponds to 0V difference,  Minimal reading is -8388608 for -VREF/2, maximum reading is +8388608 for +VREF/2.

## Firmware flowchart.

![Firmware flowchart](L432KC_SIM/Docs/SIM_flowchart.png)

## Noise
The RMS noise at higher rates depends on program behavior.
The single data transfer (chunk size = 1) shows smaller noise.
This is due to the PCB signalling is more synchronous with the ADC sampling.
The overall data rate is also faster with single data transfers because the 
transfer time overlaps with ADC conversion time.

Note. The interrrupt driven program may result with higher system noise because 
of program flow is less synchronous with the ADC sampling. 

