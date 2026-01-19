#!/usr/bin/env python3 
import argparse
import time
import subprocess
from tqdm import tqdm
def timmer(usertime, title , desc):
    if(len(title)==0):
        title ="The Timmer has stop"
        desc ="Timer reached it's end"
    pbar = tqdm(total=usertime, desc="Timer", unit="s", colour='green',bar_format='{desc}: {percentage:3.0f}%|{bar}| remaining:{remaining}')
    for i in range(usertime):
        time.sleep(1)
        pbar.update(1)
        percent = (pbar.n / usertime) * 100
        if 50 <= percent < 80:
            pbar.colour = 'yellow'
        elif percent >= 80:
            pbar.colour = 'red'
        pbar.refresh()
    pbar.close()
    subprocess.run(["notify-send",f"{title}", f"{desc}"])
def alarm():
    ""
parse =argparse.ArgumentParser(prog="Timelit")
group = parse.add_mutually_exclusive_group(required=True)
group.add_argument("-t" ,nargs=3 , metavar=("FORMAT= hh-mm-ss/ss" , "TITLE" ,"DESCRIPTION"), help="Timmer Mode")
group.add_argument("-a",help="Alarm Mode")
arge = parse.parse_args()
if(arge.t):
   
    str = arge.t[0].split("-")
    if(len(str) == 1):
        timmer(int(str[0]) , arge.t[1], arge.t[2])
    else:
        hour = 3600 * int(str[0])
        min = 60* int(str[1])
        sec= int(str[2])
        total = hour + min + sec
        timmer(total,arge.t[1], arge.t[2])
    

elif(arge.alarm):
    alarm()

