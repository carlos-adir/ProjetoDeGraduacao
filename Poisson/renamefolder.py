import os
from datetime import datetime

data = datetime.now()
year = data.year
mes = data.month
day = data.day
hour = data.hour
minu = data.minute

os.system("mv results/ results_%d.%d.%d-%d:%d" % (year, mes, day, hour, minu))

