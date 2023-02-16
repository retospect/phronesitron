from subprocess import Popen, PIPE, STDOUT
import sys

def test_phronesitron_help():
    ''' Checks that the commandline install works '''
    p = Popen(
        [sys.executable, "ph"], stdout=PIPE, stderr=STDOUT
    )
    out, _ = p.communicate()
    assert "very random" in out.decode("utf-8", "replace")
