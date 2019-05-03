def convertTime(timeString):
    timeArr = timeString.split(':')
    time = int(timeArr[0])*60 + int(timeArr[1])
    return time

def revConvertTime(timeInt):
    timeHr = timeInt/60
    timeMin = timeInt%60
    return str(timeHr) + ':' + str(timeMin)

