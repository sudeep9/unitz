
from unitz import unit, done
import logging
import subprocess

log = logging.getLogger(__name__)

#####################################################################
# Unit: run_command
#####################################################################

@unit('run_command')
def run_command(cmd, errordup = False, background = False, ignore_error = False):
    log.debug("errordup: %s", errordup)
    
    o_status_code = 0
    o_stdout = None
    o_stderr = None

    if errordup:
        o_stderr = subprocess.STDOUT
    else:
        o_stderr = subprocess.PIPE

    log.info("command: %s", cmd)
    if background:
        out = subprocess.Popen(cmd ,shell=True)
        o_status_code = [0]
        o_stdout = None
        o_stderr = None
    else:
        out = subprocess.Popen(cmd ,shell=True, stdout=subprocess.PIPE, stderr=o_stderr)
        o_status_code = out.returncode
        o_stdout = out.communicate()[0].split('\n')

    
    unit_status = True
    if not ignore_error and (o_status_code is not None and o_status_code != 0):
        unit_status = False

    return done(unit_status)


@unit('print_stream')
def print_stream(stream):
    if not stream:
        return
        
    for line in stream:
        print line
        
    return done()
