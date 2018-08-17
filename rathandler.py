from subprocess import Popen
import sys

filename = "vk_rat_kick_rewrite.py"
while True:
    print("\nStarting " + filename)
    p = Popen("python " + filename, shell=True)
    p.wait()
