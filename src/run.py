import sys

import data_format
import freq_count
import translator

sys.modules['data_format'].__dict__.clear()
sys.modules['freq_count'].__dict__.clear()
sys.modules['translator'].__dict__.clear()
