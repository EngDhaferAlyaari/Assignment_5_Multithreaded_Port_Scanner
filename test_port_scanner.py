"""Local tests for the multithreaded port scanner. No external host is scanned."""

import contextlib
import io
import socket
import unittest
from unittest.mock import patch

import port_scanner


class PortScannerTests(unittest.TestCase):
    def test_local_open_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(("127.0.0.1", 0))
            server.listen(5)
            self.assertTrue(port_scanner.check_port("127.0.0.1", server.getsockname()[1], 0.5))

    def test_local_closed_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as temporary:
            temporary.bind(("127.0.0.1", 0))
            port = temporary.getsockname()[1]
        self.assertFalse(port_scanner.check_port("127.0.0.1", port, 0.5))

    def test_multiport_results_and_summary(self):
        def fake_check(ip, port, timeout):
            return port in (100, 102)
        output = io.StringIO()
        with patch.object(port_scanner, "check_port", side_effect=fake_check), contextlib.redirect_stdout(output):
            matches = port_scanner.scan_ports("127.0.0.1", 100, 103, 0.2, 4)
        self.assertEqual(matches, [100, 102])
        self.assertIn("Open ports: 2", output.getvalue())
        self.assertIn("Not open / unreachable: 2", output.getvalue())
        self.assertIn("Elapsed time:", output.getvalue())

    def test_show_all_option(self):
        output = io.StringIO()
        with patch.object(port_scanner, "check_port", return_value=False), contextlib.redirect_stdout(output):
            port_scanner.scan_ports("127.0.0.1", 100, 100, 0.2, 1, show_all=True)
        self.assertIn("[NOT OPEN] Port 100", output.getvalue())

    def test_nonresponsive_address_no_crash(self):
        # A local mock simulates a connection timeout. No external network is contacted.
        def timed_out(ip, port, timeout):
            raise socket.timeout()
        # The production check_port handles socket timeout as OSError.
        with patch.object(port_scanner.socket, "socket") as fake_socket:
            fake_client = fake_socket.return_value.__enter__.return_value
            fake_client.connect_ex.side_effect = socket.timeout()
            self.assertFalse(port_scanner.check_port("192.0.2.1", 80, 0.1))

    def test_default_scan_range(self):
        args = port_scanner.build_parser().parse_args(["127.0.0.1"])
        self.assertEqual((args.start, args.end, args.workers), (1, 1024, 50))

    def test_reject_invalid_ip(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                port_scanner.main(["not_an_ip"])
        self.assertEqual(error.exception.code, 2)

    def test_reject_invalid_port_range(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                port_scanner.main(["127.0.0.1", "--start", "200", "--end", "100"])

    def test_reject_too_many_ports(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                port_scanner.main(["127.0.0.1", "--end", "1025"])

    def test_reject_too_many_threads(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                port_scanner.main(["127.0.0.1", "--workers", "51"])

    def test_reject_bad_timeout(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                port_scanner.main(["127.0.0.1", "--timeout", "-1"])

    def test_single_local_open_port_cli(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(("127.0.0.1", 0))
            server.listen(5)
            port = server.getsockname()[1]
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exit_code = port_scanner.main(["127.0.0.1", "--start", str(port), "--end", str(port)])
            self.assertEqual(exit_code, 0)
            self.assertIn(f"[OPEN] Port {port}", output.getvalue())

    def test_up_to_1024_ports_using_mock(self):
        output = io.StringIO()
        with patch.object(port_scanner, "check_port", return_value=False), contextlib.redirect_stdout(output):
            ports = port_scanner.scan_ports("127.0.0.1", 1, 1024, 0.1, 50)
        self.assertEqual(ports, [])
        self.assertIn("Not open / unreachable: 1024", output.getvalue())


if __name__ == "__main__":
    unittest.main()
