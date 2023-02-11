from subprocess import Popen, PIPE, STDOUT
import sys


def test_flit_help():
    p = Popen(
        [sys.executable, "-m", "ph", "--help"], stdout=PIPE, stderr=STDOUT
    )
    out, _ = p.communicate()
    assert "very random" in out.decode("utf-8", "replace")
