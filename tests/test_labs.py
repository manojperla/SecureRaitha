import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import unittest

from lab import catalog
from tooling.verify import verify

ROOT = Path(__file__).resolve().parents[1]


class LabsTest(unittest.TestCase):
    def test_all_variants(self):
        for item in catalog():
            for fixed in (False, True):
                with self.subTest(lab=item['id'], fixed=fixed):
                    with socket.socket() as temporary:
                        temporary.bind(('127.0.0.1', 0))
                        port = temporary.getsockname()[1]
                    env = dict(os.environ, LAB_KIND=item['category'], LAB_PORT=str(port),
                               LAB_HOST='127.0.0.1', LAB_FIXED=str(int(fixed)))
                    process = subprocess.Popen([sys.executable, str(ROOT / 'tooling' / 'target.py')], env=env)
                    try:
                        deadline = time.monotonic() + 10
                        while True:
                            if process.poll() is not None:
                                self.fail('Target exited before readiness')
                            try:
                                with socket.create_connection(('127.0.0.1', port), timeout=.2):
                                    break
                            except OSError:
                                if time.monotonic() > deadline:
                                    self.fail('Target did not start')
                                time.sleep(.05)
                        verify(item['category'], port, fixed)
                    finally:
                        process.terminate()
                        process.wait(timeout=5)


if __name__ == '__main__':
    unittest.main()
