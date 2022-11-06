from xled.control import HighControlInterface
from xled.discover import xdiscover


for i in xdiscover(timeout = 2):
    print(i)
