# Procman configuration for SIM board"""
__version__ = 'v0.0.1 2025-12-20'
import os
rootDir = os.environ['HOME']
py = rootDir +'/venv/bin/python -m'
simDir = rootDir +'/github/SIM_LR02/'

# abbreviations:
help,cmd,proc,cd,shell = ['help','cmd','process','cd','shell']
def  _screen(name, cmd): return f'screen -h 1000 -dmS {name} {cmd}'

#``````````````````Properties, used by procman`````````````````````````````````
title = 'Testing of the SIM board'

startup = {
'SIM server':{help:'LiteServer of the SIM board',
  cd:	simDir,
  cmd:_screen('sim', f'{py} sim -ilocalhost -p9700 -b 115200'),
  proc: 'sim -ilocalhost -p9700',
  shell: True,
  },
'SIM page':{help:'Control page for SIM board',
  cd:	simDir,
  cmd:f'{py} pypeto -f config/SIM',
  proc:'pypeto -f config/PoF_SIM',
  shell: True,
  },
'SIM plot':{help:'Plot Mean, RMS and Point-to-point amplitude',
  cmd:  f'{py} pvplot -a "L:localhost;9700:dev1:" "mean rms p2p"',
  proc: 'pvplot -a "L:localhost;9700:dev1:" "mean rms p2p"',
  shell: True,
  },
'List serial ports': {help:'List of available serial ports',
  cmd: f'xterm -e bash -c "{py} serial.tools.list_ports; exec bash"',
  shell: True,
  },
'DX-LR02':{help: 'Configuration and listening Lora modem DX-LR02 on /dev/ttyUSB1',
  cd: f'{rootDir}/github/loramodem',
  cmd: f'xterm -e bash -c "{py} loramodem -b9600 -d /dev/ttyUSB1 \'+++;AT+HELP;+++\'; {py} loramodem -h; exec bash"',
  shell: True,
  },
'Miniterm':{help:'Connect to serial port on Nucleo STM32L432KC',
  cmd:  f'lxterminal -e {py} serial.tools.miniterm /dev/ttyUSB0 115200',
  proc: 'serial.tools.miniterm /dev/ttyUSB0 115200',
  #shell: True,
  },
'Scrot':{help:'Capture part of screen.',
  cmd:  'scrot -s',
  },
'htop':{help:'Process viewer in separate xterm',
  cmd:'xterm htop',
  },
}
