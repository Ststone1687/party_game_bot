import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

a = 0
try:
    with time_limit(1):
        for i in range(10000000):
          a += 1
except TimeoutException:
    print("Timed out!")
print(a)
#1366610
#2007097
#2056302
#4086006
#2752139
#1870517