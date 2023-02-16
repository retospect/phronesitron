from subprocess import Popen, PIPE, STDOUT
import sys

def test_phronesitron_help():
    ''' Checks that the commandline install works '''
    p = Popen( ["ph"], stdout=PIPE, stderr=STDOUT
    )
    out, _ = p.communicate()
    output = out.decode("utf-8", "replace")
    print(output)
    assert "very random" in output
