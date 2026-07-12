__version__ = 'v0.1.6 2025-10-22'# 
import os
home = os.environ['HOME']
epics_home = os.environ.get('EPICS_HOME')
pypath = home +'/venv/bin/python -m'
def  _screen(name, cmd): return f'screen -h 1000 -dmS {name} {cmd}'

# abbreviations:
help,cmd,process,cd = ['help','cmd','process','cd']

#``````````````````Properties, used by manman`````````````````````````````````
title = 'Peak Simulator'
startup = {
'peakSimulator':{help:
  'Lite server, simulating peaks and noise',
  cmd:	_screen('peaksim',
    f'{pypath} liteserver.device.litePeakSimulator -ilocalhost -p9701'),
  process:	'litePeakSimulator -ilocalhost -p9701',
  },
'plot it':{help:
  'Plotting tool for peakSimulator',
  cmd:		 f'{pypath} pvplot -aL:localhost;9701:dev1: x,y',
  process:	'pvplot -aL:localhost;9701:dev1: x,y',
  },
'control it':{help:
  'Automatic parameter editing tool of the peakSimulator',
  cmd:		f'{pypath} pypeto -aLITE localhost;9701:dev1',
  process:	'pypeto -aLITE localhost;9701:dev1',
  },
'control&plot':{help:
  'Parameter editing with integrated plot',
  cmd:		f'{pypath} pypeto -c config -f peakSimPlot',
  process:	'pypeto -c config -f peakSimPlot',
  #Note: It will look for config file: config/peakSimPlot_pp.py
  },
}
#       Managers for testing and debugging
startup.update({
'tst_sleep30':{help:
  'sleep for 30 seconds', 
  cmd:'sleep 30', process:'sleep 30'
  },
})
