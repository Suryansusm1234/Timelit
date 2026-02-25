#!/usr/bin/env python3 
import argparse
import time
import subprocess
import re
from tqdm import tqdm
import curses
import time

def timmer():
    def parse_time(timestr):
        # normalize common separators (allow hh-mm-ss as well)
        timestr = timestr.strip()
        timestr = timestr.replace('-', ':')

        if ":" in timestr:
            parts = list(map(int, timestr.split(":")))
            if len(parts) == 3:
                h, m, s = parts
            elif len(parts) == 2:
                h = 0
                m, s = parts
            else:
                raise ValueError
            return h * 3600 + m * 60 + s

        pattern = r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?'
        match = re.fullmatch(pattern, timestr)

        if match:
            h = int(match.group(1) or 0)
            m = int(match.group(2) or 0)
            s = int(match.group(3) or 0)
            return h * 3600 + m * 60 + s

        if timestr.isdigit():
            return int(timestr)

        raise ValueError

    def format_time(seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02}:{m:02}:{s:02}"

    def safe_addstr(win, y, x, s, attr=0):
        try:
            h, w = win.getmaxyx()
        except Exception:
            return

        if y < 0 or y >= h:
            return

        if x < 0:
            x = 0

        if x >= w:
            return

        maxlen = w - x
        disp = s
        if len(disp) > maxlen:
            disp = disp[:maxlen]

        try:
            if attr:
                win.addstr(y, x, disp, attr)
            else:
                win.addstr(y, x, disp)
        except curses.error:
            return

    def timer_app(stdscr):
        curses.curs_set(1)
        stdscr.nodelay(True)
        stdscr.timeout(100)

        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

        fields = ["time", "title", "desc"]
        current_field = 0

        input_data = {"time": "", "title": "", "desc": ""}

        total_time = 0
        remaining = 0
        running = False
        status_msg = ""
        status_until = 0

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()

            safe_addstr(stdscr, 2, w // 2 - 6, "⏳ Timer", curses.A_BOLD)

            # Draw fields
            for idx, field in enumerate(fields):
                label = field.upper() + ": "
                y = 4 + idx * 2

                if idx == current_field and not running:
                    stdscr.attron(curses.A_REVERSE)

                safe_addstr(stdscr, y, 4, label + input_data[field])

                if idx == current_field and not running:
                    stdscr.attroff(curses.A_REVERSE)

            # Timer display
            color = 1 if running else 2
            attr = curses.color_pair(color) | curses.A_BOLD
            safe_addstr(stdscr, 12, w // 2 - 4, format_time(remaining), attr)

            safe_addstr(stdscr, 14, 4, "TAB: Switch Field | S: Start | R: Reset | Q: Quit")

            # transient status message
            if status_until > time.time():
                safe_addstr(stdscr, 16, 4, status_msg, curses.color_pair(2))

            stdscr.refresh()

            key = stdscr.getch()

            if key == ord('q'):
                break

            elif key == ord('\t') and not running:
                current_field = (current_field + 1) % len(fields)

            elif key == ord('r'):
                input_data = {"time": "", "title": "", "desc": ""}
                running = False
                remaining = 0

            elif key == ord('s') and not running:
                try:
                    total_time = parse_time(input_data["time"])
                except Exception:
                    status_msg = "Invalid time format (use ss or hh:mm:ss or hh-mm-ss)"
                    status_until = time.time() + 2.0
                    continue

                remaining = total_time
                running = True
                start_time = time.time()

                # Handle defaults
                title = input_data["title"].strip()
                desc = input_data["desc"].strip()

                if not title:
                    title = "Timer is running"

                subprocess.run(["notify-send", title, desc])

            elif key in (curses.KEY_BACKSPACE, 127) and not running:
                field_name = fields[current_field]
                input_data[field_name] = input_data[field_name][:-1]

            elif not running and key != -1 and 32 <= key <= 126:
                field_name = fields[current_field]
                input_data[field_name] += chr(key)

            if running:
                elapsed = int(time.time() - start_time)
                remaining = total_time - elapsed

                if remaining <= 0:
                    running = False
                    remaining = 0

                    end_title = input_data["title"].strip() or "Timer Finished"
                    end_desc = input_data["desc"].strip() or "Time is up!"

                    subprocess.run(["notify-send", end_title, end_desc])

            time.sleep(0.05)

    try:
        curses.wrapper(timer_app)
    except Exception:
        # fallback to console progress bar
        usertime = 0
        # If terminal fallback is desired but no time provided, just return
        return
def stopwatch():
    def format_time(elapsed):
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        milliseconds = int((elapsed - int(elapsed)) * 100)
        return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}"


    def draw_center(stdscr, text, y_offset=0, color_pair=0, bold=False):
        h, w = stdscr.getmaxyx()
        x = w // 2 - len(text) // 2
        y = h // 2 + y_offset

        if bold:
            stdscr.attron(curses.A_BOLD)
        if color_pair:
            stdscr.attron(curses.color_pair(color_pair))

        stdscr.addstr(y, x, text)

        if color_pair:
            stdscr.attroff(curses.color_pair(color_pair))
        if bold:
            stdscr.attroff(curses.A_BOLD)


    def stopwatch_inner(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.timeout(50)

        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

        start_time = 0
        elapsed = 0
        running = False
        laps = []

        while True:
            stdscr.clear()

            if running:
                elapsed = time.time() - start_time

            # Title
            draw_center(stdscr, "⏱  Stopwatch by Suryansu", -4, 3, True)

            # Time Display
            draw_center(stdscr, format_time(elapsed), 0, 1, True)

            # Status
            status_text = "RUNNING" if running else "PAUSED"
            status_color = 1 if running else 2
            draw_center(stdscr, f"[ {status_text} ]", 2, status_color, True)

            # Controls
            stdscr.addstr(2, 2, "SPACE: Start/Pause  |  L: Lap  |  R: Reset  |  Q: Quit")

            # Laps
            stdscr.addstr(4, 2, "Laps:")
            for i, lap in enumerate(laps[-5:], 1):  # show last 5 laps
                stdscr.addstr(5 + i, 4, f"{len(laps)-5+i if len(laps)>=5 else i}. {lap}")

            stdscr.refresh()

            key = stdscr.getch()

            if key == ord('q'):
                break

            elif key == ord(' '):  # SPACE
                if running:
                    running = False
                else:
                    start_time = time.time() - elapsed
                    running = True

            elif key == ord('r'):
                running = False
                elapsed = 0
                laps = []

            elif key == ord('l') and running:
                laps.append(format_time(elapsed))

            time.sleep(0.02)

    curses.wrapper(stopwatch_inner)

parse =argparse.ArgumentParser(prog="Timelit")
group = parse.add_mutually_exclusive_group(required=True)
group.add_argument("-t" ,help = "Timmer mode", action="store_true")
group.add_argument("-s", help="Stopwatch mode", action="store_true")
arge = parse.parse_args()
if(arge.t):
   
    # str = arge.t[0].split("-")
    # if(len(str) == 1):
    #     timmer(int(str[0]) , arge.t[1], arge.t[2])
    # else:
    #     hour = 3600 * int(str[0])
    #     min = 60* int(str[1])
    #     sec= int(str[2])
    #     total = hour + min + sec total,arge.t[1], arge.t[2]
        timmer()
    

elif(arge.s):
    stopwatch()


