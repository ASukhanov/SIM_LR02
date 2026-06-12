/*
 * board.h
 *
 *  Created on: 2026-05-30
 *      Author: andrey
 */
/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __BOARD_H
#define __BOARD_H
#define VERSION "1.0.6"//2026-06-10 Baud rate changed to 115200. Stop sending samples if no command received, recLimit default value changed to 0, LED_GREEN fires on board_report, flush Uart in board init
void board_init(SPI_HandleTypeDef* hptr);

//`````````````````Abbreviations, corrected
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

//	Defines
#define SER_START_CHAR '<' //Start character for serial communication
#define SER_END_CHAR '>'   //End character for serial communication
//#define POLLING_INTERVAL 10 //ms
//#define REPORTING_INTERVAL 1000//ms

#define UART1_RXSIZE 16
#define DATACHUNKSIZE 1// Larger chunks cause excessive noise and transfer speed is effectively lower because for single dtransfer the transfer delay overlaps with with conversion.
#define LARGEST(x,y) ( (x) > (y) ? (x) : (y) )
#define UART1_TXSIZE LARGEST(80,10*DATACHUNKSIZE+4)//10 chars per word + <> and \n
struct DATACHUNK{
  uint8_t len;
  uint8_t size;
  int32_t buf[DATACHUNKSIZE];
};
struct BOARD_RESULT{
  uint32_t sampleCount;	//Number of ADC samples, taken since last report
  uint32_t n;		//Number of samples, accumulated for statistics calculation
  int32_t mean;		//10 * Mean
  int32_t stdev;	//10 * Standard deviation
  int32_t peak2peak;	//Peak-to-peak amplitude
  uint32_t clockCount;	//milliseconds
};
/* Private function prototypes -----------------------------------------------*/
void dbgUart_printf(const char* format, ...);
void uart_printf(const char* format, ...);
void uart_hexdump(const char* prefix, uint8_t*, uint8_t len);
void printe(char* msg);

void board_init(SPI_HandleTypeDef* hspiPtr);
void board_process_cmd(char *buf);
int board_acquire_sample();// called in the main loop
struct BOARD_RESULT board_report();//

extern uint16_t receiveTimeout;
extern uint16_t reportingInterval;
extern uint16_t recLimit;

#endif /* __BOARD_H */