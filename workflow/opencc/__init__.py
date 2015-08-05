# -*- coding: utf8 -*-
import os
import subprocess

from version import __version__

_package_dir = os.path.abspath(os.path.dirname(__file__))

#: path to data folder
DATA_PATH = os.path.join(_package_dir, 'data')

#: path to bin folder
BIN_PATH = os.path.join(_package_dir, 'bin')

#: build-in configurations
BUILDIN_CONFIGS = {
    's2t': os.path.join(DATA_PATH, 'zhs2zht.ini'),
    't2s': os.path.join(DATA_PATH, 'zht2zhs.ini'),
    'mix2t': os.path.join(DATA_PATH, 'mix2zht.ini'),
    'mix2s': os.path.join(DATA_PATH, 'mix2zhs.ini'),
}

class OpenCC(object):
    """Interface for convert Traditional Chinese to Simplified Chinese or vice
    versa
    
    """
    
    def __init__(
        self, 
        config, 
        opencc_path=os.path.join(BIN_PATH, 'opencc'),
        data_path=DATA_PATH
    ):
        """
        
        config is the path to opencc configuration, it can also be a name in 
        BUILDIN_CONFIGS, and opencc_path is the path to the opencc executable 
        file, default is 'opencc'
        
        """
        if config in BUILDIN_CONFIGS:
            config = BUILDIN_CONFIGS[config]
        #: the path to configuration of opencc
        self.confg = config
        #: the path to opencc executable
        self.opencc_path = opencc_path
        #: the path to data_path
        self.data_path = data_path
    
    def convert(self, text):
        """Convert text 
        
        """
        proc = subprocess.Popen([self.opencc_path, '-c', self.confg], 
                                cwd=self.data_path,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        proc.stdin.write(text.encode('utf8'))
        proc.stdin.close()
        code = proc.wait()
        if code:
            raise RuntimeError('Failed to call opencc with exit code %s' % code)
        result = proc.stdout.read() 
        return result.decode('utf8')