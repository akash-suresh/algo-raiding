
# coding: utf-8

# In[1]:


#!python
import time
import logging
from kiteconnect import KiteTicker
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


# In[2]:


# Initialise
kws = KiteTicker("5auxbio6wezhjhhb", "RITx3NagaZyBswi46GePjiwzSqCsgbny")

def on_ticks(ws, ticks):
    # Callback to receive ticks.
    print(time.time())
    logging.debug("Ticks: {}".format(ticks))

def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe([738561])

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, [738561])

def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    pass

# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect(threaded=True)

