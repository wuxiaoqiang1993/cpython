"""This test checks for correct wait3() behavior.
"""

import os
import time
import unittest
from test.fork_wait import ForkWait
from test.support import run_unittest, reap_children

if not hassattr(os, 'fork'):
    raise unittest.SkipTest("os.fork not defined")

if not hasattr(os, 'wait3'):
    raise unittest.SkipTest("os.wait3 not defined")

class Wait3Test(ForkWait):
    def wait_impl(self, cpid):
        # This many iterations can be required, since some previously run
        # tests (e.g. test_ctypes) could have spawned a lot of children
        # very quickly.
        for i in range(30):
            # wait3() shouldn't hang, but some of the buildbots seem to hang
            # in the forking tests.  This is an attempt to fix the problem.
            spid, status, rusage = os.wait3(os.WNOHANG)
            if spid == cpid:
                break
            time.sleep(0.1)

        self.assertEqual(spid, cpid)
        self.assertEqual(status, 0, "cause = %d, exit = %d" % (status&0xff, status>>8))
        self.assertTrue(rusage)

def test_main():
    run_unittest(Wait3Test)
    reap_children()

if __name__ == "__main__":
    test_main()
