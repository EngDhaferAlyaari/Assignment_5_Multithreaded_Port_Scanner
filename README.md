# Assignment 5 - Multithreaded Port Scanner

**Student:** Eng. Dhafer Alyaari  
**Language:** Python

## English

This program checks TCP ports on a target IPv4 address using multiple threads.

- It uses `socket` to connect to ports and `ThreadPoolExecutor` to run up to 50 checks at the same time.
- It prints open ports and shows the total scan time.
- It handles connection timeouts and invalid IP addresses.
- It scans ports **1 to 1024** by default.

**Run:**

```bash
python port_scanner.py 127.0.0.1
```

To scan a smaller range:

```bash
python port_scanner.py 127.0.0.1 --start 20 --end 100 --timeout 0.5 --workers 50
```

To display ports that did not accept a connection, add `--show-all`.

## بالعربية

برنامج بسيط لفحص منافذ TCP لعنوان IP باستخدام الخيوط المتعددة.

- يستخدم `socket` للاتصال بالمنافذ، و`ThreadPoolExecutor` لتشغيل الفحص بالتوازي.
- يعرض المنافذ المفتوحة ومدة الفحص.
- يعالج انتهاء مهلة الاتصال والعناوين غير الصحيحة.
- يفحص المنافذ من **1 إلى 1024** افتراضيًا.

**مثال التشغيل:**

```bash
python port_scanner.py 127.0.0.1
```

## Example output / مثال النتيجة

```text
Target IP: 127.0.0.1
Ports: 8000-8002
Threads: 3
--------------------------------------------
[OPEN] Port 8000
--------------------------------------------
Open ports: 1
Not open / unreachable: 2
Elapsed time: 0.01 seconds
```

*Example only: open ports and elapsed time depend on the computer.*  
*المثال توضيحي؛ المنافذ المفتوحة والزمن يختلفان حسب الجهاز.*

## Files / الملفات

- `port_scanner.py` - Source code / الكود الأساسي.
- `test_port_scanner.py` - Local tests / اختبارات محلية.
- `Run_Test.bat` - Runs tests on Windows / تشغيل الاختبارات في ويندوز.
- `Example_Output.txt` - Example result / مثال نتيجة.
- `.github/workflows/build-windows.yml` - Builds a Windows EXE on GitHub Actions.

**Windows EXE:** The GitHub workflow builds `Port_Scanner.exe` on a Windows runner. It is not included in this ZIP until that workflow completes successfully. See `WINDOWS_EXE_INSTRUCTIONS.md`.

**Note:** Only scan devices that you own or are permitted to test. An unsuccessful TCP connection can mean a closed or filtered port; the scanner does not distinguish the two.
