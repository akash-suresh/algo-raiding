from classes.RenkoEntry import Renko
import logging


#
# def getNewRenko(lastRenko, minute, brickHeight):
#     if minute.listPrice >= lastRenko.high + brickHeight:
#         renko = Renko(minute.listPrice - brickHeight, minute.listPrice, 1, minute.time)
#     elif minute.listPrice <= lastRenko.low - brickHeight:
#         renko = Renko(minute.listPrice, minute.listPrice + brickHeight, -1, minute.time)
#     else:
#         return None
#     return renko

def getNewRenko(lastRenko, minute, brickHeight):
    if minute.listPrice >= lastRenko.high + brickHeight:
        renko = Renko(lastRenko.high, lastRenko.high + brickHeight, 1, minute.time)
    elif minute.listPrice <= lastRenko.low - brickHeight:
        renko = Renko(lastRenko.low - brickHeight, lastRenko.low, -1, minute.time)
    else:
        return None
    return renko


# def printRenkoDeque(renkoDeque):
#     if len(renkoDeque)>0:
#         for i in renkoDeque:
#             i.toString()
#     else:
#         print('empty')

def printRenkoDeque(renkoDeque):
    # logging.debug('size of queue: {}'.format(len(renkoDeque)))
    if len(renkoDeque)>0:
        for i in renkoDeque:
            i.toString(True)
    else:
        logging.debug('empty queue')

def generateRenko(minute, renkoDeque, brickHeight, stepCount, verbose):
    # import pdb;pdb.set_trace()
    size = len(renkoDeque)
    if size == 0:
        newRenko = Renko(minute.listPrice, minute.listPrice, 0, minute.time)
        newRenko.toString(verbose)
        renkoDeque.append(newRenko)
    else:
        lastRenko = renkoDeque[-1]
        newRenko = getNewRenko(lastRenko, minute, brickHeight)
        if newRenko:
            if size == stepCount:
                renkoDeque.popleft()
            renkoDeque.append(newRenko)
            newRenko.toString(verbose)
    return renkoDeque, newRenko
# low: 119.75, high: 119.8,
# 1 = 119.85
# 2 = 119.9
def getEmotion(renkoDeque):
    emotion = 0
    for renko in renkoDeque:
        emotion += renko.renkoType
    return emotion

def renkoExitLogic(renkoDeque, stepCount, boughtFlag):
    emotion = getEmotion(renkoDeque)
    logging.debug("emotion : {}".format(emotion))
    if abs(emotion) == stepCount - 2:
        lastRenko = renkoDeque[-1]
        if lastRenko.renkoType == -1 * boughtFlag:
            logging.debug("renkoExit : {}".format(lastRenko.renkoType == -1 * boughtFlag))
            return True
    return False
