# Build the Windows EXE without a computer

The assignment is in **Python**, not C. To produce the Windows executable `Port_Scanner.exe`, the included GitHub Actions workflow must run on a Windows runner. PyInstaller cannot make a Windows executable on Linux.

## Using your phone and GitHub

1. Create a **Public** GitHub repository named `Assignment_5_Multithreaded_Port_Scanner`.
2. Upload these files: `port_scanner.py`, `test_port_scanner.py`, `README.md`, `Run_Test.bat`, `Run_Scanner.bat`, `Example_Output.txt`, and this instruction file.
3. **Important:** GitHub Actions only recognizes the build file at the precise path `.github/workflows/build-windows.yml`. Uploading it at the repository root will not work.
4. In the GitHub website, select **Add file > Create new file**. Type the filename `.github/workflows/build-windows.yml`. Paste the content from the included workflow file, then select **Commit changes**. The workflow's first run starts when committed.
5. Open the **Actions** tab and select **Build Windows EXE**. If prompted, enable GitHub Actions. You can also select **Run workflow** manually.
6. When the run succeeds, the workflow uploads a `Port_Scanner_Windows` artifact and attempts to commit `Port_Scanner.exe` to your repository automatically. If GitHub blocks the commit due to repository permission settings, download the artifact in Actions and upload `Port_Scanner.exe` manually using your phone.
7. The trainer can then view the Python code, read README, and download the Windows program from the repository.

**Do not upload or rename a Linux executable as `.exe`.** This ZIP intentionally does not claim to contain a Windows EXE before it is built and verified.

Use the scanner only on devices you own or have explicit authorization to test.
