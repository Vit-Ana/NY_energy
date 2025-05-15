"""
A convenient way to write simple messages to stdout and a 
log file as well. Usage:

   ql = quicklog.logger()
   ql = quicklog.logger(filename)
   ql.log(string,value,oneline=False,json=False)
   ql.info(string,dataframe)
   ql.close()

Jul 2021 PJW
"""

import pandas as pd
import sys 
import os
import io
from json import dumps
import __main__

class logger():

    def __init__(self,logfile=None):
        """Start logging."""
        if logfile is None:
            logfile = os.path.basename(__main__.__file__)
            logfile = logfile.replace(".py",".log")
        self.lfh = open(logfile,'w')
        self.handles = [sys.stdout,self.lfh]

    def close(self):
        """Stop logging."""
        if self.lfh is not None: 
            self.lfh.close()
            self.handles = [sys.stdout]
       
    def log(self,message,value=None,oneline=False,json=False):
        """Write a log message."""
        for fh in self.handles:
            if value is not None:
                if type(value) == pd.Series or type(value) == pd.DataFrame:
                    print( f'\n{message}:', file=fh, flush=True )
                    print( value.to_string(), file=fh, flush=True )
                else:
                    if oneline:
                        print( f'{message}: {value}', file=fh, flush=True )
                    else:
                        if json==False:
                            print( f'\n{message}:\n{value}', file=fh, flush=True )
                        else:
                            if type(value) == set:
                                jvalue = dumps(list(value),indent=4)
                            else:
                                jvalue = dumps(value,indent=4)
                            print( f'\n{message}:\n{jvalue}', file=fh, flush=True )
            else:
                print( message, file=fh, flush=True )

    def info(self,message,df):
        """Write a dataframe's info to the log"""
        buffer = io.StringIO()
        df.info(buf=buffer)
        self.log(message,buffer.getvalue())

    def line(self,message,value=None):
        """Write a one-line log message."""
        self.log(message,value,oneline=True)

