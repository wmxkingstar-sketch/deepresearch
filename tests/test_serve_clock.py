import unittest

from serve_clock import DEFAULT_HOST, DEFAULT_PORT, format_url, parse_args, resolve_app_dir


class ServeClockTests(unittest.TestCase):
    def test_parse_args_uses_defaults(self) -> None:
        args = parse_args([])

        self.assertEqual(args.host, DEFAULT_HOST)
        self.assertEqual(args.port, DEFAULT_PORT)

    def test_parse_args_accepts_custom_values(self) -> None:
        args = parse_args(["--host", "0.0.0.0", "--port", "9001"])

        self.assertEqual(args.host, "0.0.0.0")
        self.assertEqual(args.port, 9001)

    def test_format_url_rewrites_wildcard_host(self) -> None:
        self.assertEqual(format_url("0.0.0.0", 8000), "http://127.0.0.1:8000")
        self.assertEqual(format_url("127.0.0.1", 9001), "http://127.0.0.1:9001")

    def test_clock_app_directory_exists(self) -> None:
        app_dir = resolve_app_dir()

        self.assertTrue(app_dir.is_dir())
        self.assertTrue((app_dir / "index.html").is_file())


if __name__ == "__main__":
    unittest.main()
