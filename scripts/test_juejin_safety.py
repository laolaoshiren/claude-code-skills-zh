#!/usr/bin/env python3
"""掘金脚本的离线安全回归；不会读取 Cookie、访问网络或创建草稿。"""

import unittest
from types import SimpleNamespace
from unittest import mock

import post_to_juejin
from post_to_juejin import publish_via_browser, validate_draft_id


class DraftIdValidationTests(unittest.TestCase):
    def test_accepts_ascii_numeric_ids(self):
        self.assertEqual(validate_draft_id(123456), "123456")
        self.assertEqual(validate_draft_id("00123"), "00123")

    def test_rejects_javascript_injection_and_non_ascii_digits(self):
        invalid_ids = (
            "123'); require('child_process').execSync('echo pwned'); ('",
            "123\n456",
            "１２３",
            "",
            None,
        )
        for draft_id in invalid_ids:
            with self.subTest(draft_id=draft_id):
                with self.assertRaises(ValueError):
                    validate_draft_id(draft_id)


class BrowserScriptEncodingTests(unittest.TestCase):
    @mock.patch("post_to_juejin.os.unlink")
    @mock.patch("post_to_juejin.subprocess.run")
    @mock.patch("post_to_juejin.tempfile.NamedTemporaryFile")
    def test_uses_utf8_for_generated_script_and_node_output(
        self, named_temp_file, run, unlink
    ):
        temporary_file = mock.MagicMock()
        temporary_file.name = "juejin-test.js"
        named_temp_file.return_value.__enter__.return_value = temporary_file
        run.return_value = SimpleNamespace(stdout="✅ 已点击发布按钮", stderr="")

        original_cookie = post_to_juejin.COOKIE_FULL
        post_to_juejin.COOKIE_FULL = "test-cookie"
        try:
            publish_via_browser("123456")
        finally:
            post_to_juejin.COOKIE_FULL = original_cookie

        named_temp_file.assert_called_once_with(
            mode="w", suffix=".js", delete=False, encoding="utf-8"
        )
        generated_script = temporary_file.write.call_args.args[0]
        self.assertIn("已点击发布按钮", generated_script)

        run_kwargs = run.call_args.kwargs
        self.assertEqual(run_kwargs["encoding"], "utf-8")
        self.assertEqual(run_kwargs["errors"], "replace")
        self.assertTrue(run_kwargs["text"])
        unlink.assert_called_once_with("juejin-test.js")


if __name__ == "__main__":
    unittest.main()
