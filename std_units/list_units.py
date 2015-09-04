
from unitz import unit, done
import logging
import subprocess

log = logging.getLogger(__name__)

@unit('nth')
def nth(src_list, n):
    o_element = src_list[n]
    return done()

@unit('slice_list')
def slice_list(src_list, from_ix = 0, end_ix = -1):
    if end_ix == -1:
        o_new_list = src_list[from_ix:]
    else:
        o_new_list = src_list[from_ix:end_ix]
    return done()
