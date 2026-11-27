"""Exercise the environment report with a kubectl that accepts the expected resources."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


class EnvironmentTests(unittest.TestCase):
    def test_environment_report_uses_only_deployments_and_autoscalers(self):
        script = Path(__file__).with_name("ambiente.sh")
        with tempfile.TemporaryDirectory() as directory:
            kubectl = Path(directory, "kubectl")
            kubectl.write_text("""#!/bin/sh
case "$*" in
    'get deployment users-api posts-api api-gateway -n test -o json'|'get hpa -n test -o json')
        echo '{"items":[]}' ;;
    *) exit 1 ;;
esac
""")
            kubectl.chmod(0o755)
            report = Path(directory, "environment.json")
            env = dict(os.environ, NAMESPACE="test", PATH=directory + os.pathsep + os.environ["PATH"])
            subprocess.run([script, report], env=env, check=True)
            data = json.loads(report.read_text())
            self.assertEqual(data["deployments"], [])
            self.assertEqual(data["autoscalers"], [])
