import numpy as np
from datetime import datetime

def current_time():
    return str(datetime.now()).split()[1][:5]