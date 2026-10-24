"""Focused dispatch workflow regressions using the local fake CLIs only."""
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import time
import unittest

import test_acceptance as helpers


class DispatchRegressions(unittest.TestCase):
    setUp = helpers.Acceptance.setUp
    fake = helpers.Acceptance.fake
    request = helpers.Acceptance.request
    cli = helpers.Acceptance.cli
    dispatch = helpers.Acceptance.dispatch

    def resume(self, dispatch_id, *extra):
        return self.cli("dispatch", "--dispatch-id", dispatch_id,
                        "--state-dir", str(self.state), *extra)

    def install_counting_copilot(self):
        counter = self.root / "active-count"
        counter.write_text("0 0")
        self.env["ACTIVE_COUNT"] = str(counter)
        body = """import fcntl,time
p=Path(os.environ['ACTIVE_COUNT'])
with p.open('r+') as f:
 fcntl.flock(f,fcntl.LOCK_EX); a,m=map(int,f.read().split()); a+=1; m=max(m,a); f.seek(0); f.truncate(); f.write(f'{a} {m}'); f.flush(); fcntl.flock(f,fcntl.LOCK_UN)
time.sleep(.35)
with p.open('r+') as f:
 fcntl.flock(f,fcntl.LOCK_EX); a,m=map(int,f.read().split()); f.seek(0); f.truncate(); f.write(f'{a-1} {m}'); f.flush(); fcntl.flock(f,fcntl.LOCK_UN)
print('completed')"""
        self.fake("copilot", body)
        return counter

    def parallel_classifications(self, files):
        def run(path):
            request = self.request(allowed_files=[path])
            for attempt in range(50):
                result = self.cli("dispatch", "--request", "-", "--state-dir", str(self.state),
                                  request=request)
                if result.returncode == 0:
                    payload = json.loads(result.stdout)
                    self.assertEqual(payload["status"], "awaiting_review", result.stdout)
                    self.assertEqual(payload["tool"], "copilot", result.stdout)
                    return payload
                if "Resource temporarily unavailable" not in result.stderr:
                    self.fail(f"dispatch failed without the recognized busy error: {result.stderr}")
                time.sleep(0.05 + attempt * 0.005)
            self.fail("dispatch remained busy after 50 bounded retries")
        with ThreadPoolExecutor(max_workers=len(files)) as pool:
            return list(pool.map(run, files))

    def claude_catalog(self):
        return {
            "models": {
                "codex": ["gpt-6.1-luna", "gpt-6.1-sol"],
                "claude": ["claude-haiku-5.5", "claude-sonnet-5.5", "claude-opus-5.5"],
            },
            "model_source": "isolated fake catalog",
        }

    def assert_task_calls_once(self, files, payloads):
        calls = [json.loads(line) for line in (self.root / "calls").read_text().splitlines()]
        self.assertEqual(len(calls), len(files))
        prompts = [argv[-1] for argv in calls]
        seen = Counter(path for path in set(files)
                       for prompt in prompts if path in prompt)
        self.assertEqual(seen, Counter(files))
        self.assertEqual(len({p["dispatch_id"] for p in payloads}), len(files))

    def test_coding_verification_retries_same_level_before_escalation(self):
        self.fake("copilot", "print('accepted report')")
        self.fake("codex", "print('accepted report')")
        started = self.dispatch(host="agy", task_type="implementation",
                                allowed_files=["src.py"])
        self.assertEqual(started["status"], "awaiting_review")
        self.assertEqual(started["level"], 2)

        first = self.resume(started["dispatch_id"], "--outcome", "verification-failed",
                            "--level", "2", "--failure-reason", "assertion failed",
                            "--feedback", "handle empty input", "--partial-work-reviewed")
        self.assertEqual(first.returncode, 0, first.stderr)
        retried = json.loads(first.stdout)
        self.assertEqual(retried["status"], "awaiting_review")
        self.assertEqual(retried["level"], 2)
        self.assertIn("assertion failed", retried["prompt"])
        self.assertIn("handle empty input", retried["prompt"])

        second = self.resume(started["dispatch_id"], "--outcome", "verification-failed",
                             "--level", "3", "--failure-reason", "still fails",
                             "--partial-work-reviewed")
        self.assertEqual(second.returncode, 0, second.stderr)
        escalated = json.loads(second.stdout)
        self.assertEqual(escalated["level"], 3)
        self.assertEqual(escalated["status"], "awaiting_review")

    def test_native_dispatch_failure_cannot_skip_level(self):
        started = self.dispatch()
        self.assertEqual(started["status"], "native_required")
        invalid = self.resume(started["dispatch_id"], "--outcome", "dispatch-failed",
                              "--level", "4", "--failure-reason", "native unavailable")
        self.assertNotEqual(invalid.returncode, 0)
        valid = self.resume(started["dispatch_id"], "--outcome", "dispatch-failed",
                             "--level", "3", "--failure-reason", "native unavailable")
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertEqual(json.loads(valid.stdout)["level"], 3)

    def test_opencode_zero_exit_json_error_is_failure_evidence(self):
        self.fake("opencode", "print(json.dumps({'type':'error','error':'quota exceeded'}))")
        result = self.dispatch(host="claude", task_type="chores", allowed_files=["notes.md"],
                               **self.claude_catalog())
        self.assertEqual(result["status"], "native_required")
        state = next(path for path in self.state.rglob("*.json")
                     if result["dispatch_id"] in path.read_text())
        saved = json.loads(state.read_text())
        attempts = saved.get("attempts", [])
        self.assertTrue(attempts)
        raw = json.dumps(attempts[0], ensure_ascii=False).lower()
        self.assertIn("quota", raw)
        self.assertIn("opencode", raw)

    def test_exhausted_is_terminal_and_does_not_relaunch(self):
        started = self.dispatch(host="claude", task_type="classification", **self.claude_catalog())
        self.assertEqual(started["status"], "native_required")
        next_stage = self.resume(started["dispatch_id"], "--outcome", "dispatch-failed",
                                 "--failure-reason", "native unavailable")
        self.assertEqual(next_stage.returncode, 0, next_stage.stderr)
        terminal = json.loads(next_stage.stdout)
        self.assertEqual(terminal["status"], "exhausted")
        before = (self.root / "calls").read_text() if (self.root / "calls").exists() else ""
        again = self.resume(started["dispatch_id"], "--outcome", "dispatch-failed",
                            "--level", "3", "--failure-reason", "retry")
        self.assertNotEqual(again.returncode, 0)
        after = (self.root / "calls").read_text() if (self.root / "calls").exists() else ""
        self.assertEqual(before, after)

    def test_research_scope_requires_sandbox_and_keeps_writes_inside(self):
        no_sandbox = self.cli("dispatch", "--request", "-", "--state-dir", str(self.state),
                              request=self.request(task_type="research", allowed_files=[],
                                                   sandbox_dir=None))
        self.assertNotEqual(no_sandbox.returncode, 0)
        sandbox = self.root / "research-sandbox"
        sandbox.mkdir()
        result = self.dispatch(task_type="research", allowed_files=[], sandbox_dir=str(sandbox))
        self.assertEqual(result["status"], "native_required")
        self.assertIn(str(sandbox), result["prompt"])

        project_scope = self.cli("dispatch", "--request", "-", "--state-dir", str(self.state),
                                 request=self.request(task_type="research", allowed_files=["../project/labels.txt"],
                                                      sandbox_dir=str(sandbox)))
        self.assertNotEqual(project_scope.returncode, 0)
        self.assertFalse((self.root / "calls").exists())

    def test_resume_preserves_original_request_and_appends_feedback(self):
        started = self.dispatch(**self.claude_catalog())
        self.fake("claude", "print('accepted report')")
        changed = self.cli("dispatch", "--dispatch-id", started["dispatch_id"],
                           "--outcome", "dispatch-failed", "--level", "2",
                           "--failure-reason", "quota", "--feedback", "preserve this",
                           "--request", "-", "--state-dir", str(self.state),
                           request=self.request(prompt="replacement request"))
        # Resume has no request option in the contract; argparse must reject it instead of
        # accepting a replacement task payload.
        self.assertNotEqual(changed.returncode, 0)
        good = self.resume(started["dispatch_id"], "--outcome", "dispatch-failed",
                           "--level", "3", "--failure-reason", "quota",
                           "--feedback", "preserve this")
        self.assertEqual(good.returncode, 0, good.stderr)
        continued = json.loads(good.stdout)
        self.assertIn(self.request()["prompt"], continued["prompt"])
        self.assertNotIn("replacement request", continued["prompt"])
        self.assertIn("preserve this", continued["prompt"])

    def test_same_file_dispatches_do_not_run_concurrently(self):
        counter = self.install_counting_copilot()
        payloads = self.parallel_classifications(["shared.txt", "shared.txt"])
        active, maximum = map(int, counter.read_text().split())
        self.assertEqual(active, 0)
        self.assertEqual(maximum, 1)
        self.assertEqual(len(payloads), 2)
        self.assert_task_calls_once(["shared.txt", "shared.txt"], payloads)

    def test_each_external_cli_is_limited_to_three_live_slots(self):
        counter = self.install_counting_copilot()
        payloads = self.parallel_classifications(["a.txt", "b.txt", "c.txt", "d.txt"])
        active, maximum = map(int, counter.read_text().split())
        self.assertEqual(active, 0)
        self.assertLessEqual(maximum, 3)
        self.assertEqual(len(payloads), 4)
        self.assert_task_calls_once(["a.txt", "b.txt", "c.txt", "d.txt"], payloads)


if __name__ == "__main__":
    unittest.main()
