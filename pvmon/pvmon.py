#!/usr/bin/env nix-shell
#!nix-shell --pure -i python3 -p python3 python3Packages.psutil pv

import sys
import os
import psutil
import subprocess as sp
import fcntl
import time
import shutil
import signal

class SubPV():
  def __init__(self, pid, width=80):
    self.pid = pid
    self.draw = ["  Starting pv..."]
    self.draw_cur = 0 # current cursor, to not resize self.draw except to increase size
    self.buf = b""
    self.pv = sp.Popen(["pv", "-d", str(pid), "-f", "-w", str(width)], stdout=sp.PIPE, stderr=sp.STDOUT)
    fcntl.fcntl(self.pv.stdout, fcntl.F_SETFL, fcntl.fcntl(self.pv.stdout, fcntl.F_GETFL) | os.O_NONBLOCK)
    self.dead = False

  def check(self):
    if self.dead:
      return False
    if self.pv.poll() is not None:
      self.dead = True
      return False

    line = self.pv.stdout.read()
    if line is None:
      return True
    self.buf += line

    # if there's only one line, pv only uses \r
    # if there's multiple lines, pv uses \r\n between lines and \r\033[A to cursor-up at the end
    # so we split by \r and handle the up and downs ourselves out of the start

    [*lines, self.buf] = self.buf.split(b'\r')
    for line in lines:
      while line.startswith(b'\n'):
        self.draw_cur += 1
        if self.draw_cur >= len(self.draw):
          self.draw += [""]
        line = line[1:]

      while line.startswith(b'\033[A'):
        self.draw_cur -= 1
        assert(self.draw_cur >= 0)
        line = line[3:]

      self.draw[self.draw_cur] = line.decode()
    return True

def scan_processes(procname):
  return [p.pid for p in psutil.process_iter(['pid', 'name']) if p.name() == procname]

def main():
  if len(sys.argv) != 2:
    print("Usage: pvmon PROCNAME")
    return

  width = shutil.get_terminal_size().columns

  pids = []
  pvs = {}
  procname = sys.argv[1]

  while True:
    for pid in scan_processes(procname):
      if pid not in pvs:
        pvs[pid] = SubPV(pid, width)
        pids += [pid]

    drawn_lines = 0
    for i, pid in enumerate(pids):
      if pvs[pid].check():
        print(f"[{i+1}] {pid}".ljust(width, " "))
        for line in pvs[pid].draw:
          print(line)
        drawn_lines += len(pvs[pid].draw) + 1

    time.sleep(0.5) # pv repaints every second so half a second is plenty
    print("\r" + "\033[A"*drawn_lines, end="")

def sigwinch(signum, frame):
  print("SIGWINCH not supported")
  exit()  
signal.signal(signal.SIGWINCH, sigwinch)

if __name__ == "__main__":
  main()
