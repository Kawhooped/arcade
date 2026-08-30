import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = 8933


def up():
    s = socket.socket()
    s.settimeout(0.3)
    try:
        s.connect(("127.0.0.1", PORT))
        return True
    except OSError:
        return False
    finally:
        s.close()


def main():
    if up():
        print("http://127.0.0.1:8933/  (already up)")
        return
    creation = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    subprocess.Popen(
        [sys.executable.replace("python.exe", "pythonw.exe"), str(ROOT / "server.py")],
        cwd=str(ROOT),
        creationflags=creation,
    )
    print("http://127.0.0.1:8933/")


if __name__ == "__main__":
    main()
