# Timelit
Timelit is a Python-based CLI timer and alarm app for Ubuntu-based Linux distributions.

## Requirements
Timelit requires the following Python and system packages:
- **tqdm** → Used for creating the progress bar
- **subprocess** → Used to run commands from Python
- **time** → For time-based operations
- **notify-send** → For sending desktop notifications (System package)
- **argparse** → For accepting arguments from the terminal

## Installation

### Prerequisites
Ensure you have Python 3.6+ installed and `notify-send` available on your system.

1. Clone or download the Timelit repository
2. Install required Python packages:
```bash
pip install tqdm
```

3. Remove the `.py` extension from the script:
```bash
mv timelit.py timelit
```

4. Make the script executable:
```bash
chmod +x timelit
```

### Global Installation
To run Timelit from anywhere in your terminal:

```bash
sudo cp timelit /usr/local/bin/timelit
sudo chmod +x /usr/local/bin/timelit
```

After this, you can run Timelit directly from any directory:
```bash
timelit -t 60 "My Timer" "Description"
```

## Usage

### Timer Mode
Run a timer with custom title and description:

```bash
timelit -t <TIME> <TITLE> <DESCRIPTION>
```

**Time Format Options:**
- Seconds only: `timelit -t 60 "My Timer" "Cooking"`
- Hours-Minutes-Seconds: `timelit -t 01-05-30 "Workout" "Rest period"`

**Examples:**
```bash
# 30-second timer
timelit -t 30 "Break" "Time for a quick break"

# 1 hour, 30 minutes, 45 seconds timer
timelit -t 01-30-45 "Study Session" "Focus time"
```

### Features
- **Color-coded progress bar** → Green (0-50%), Yellow (50-80%), Red (80-100%)
- **Desktop notifications** → Automatic notification when timer completes
- **Custom titles and descriptions** → Personalize your timers
- **Real-time progress tracking** → Visual feedback with remaining time

## Notes
- The timer runs in the foreground; use `&` to run in the background
- Desktop notifications require `notify-send` to be installed
- Alarm functionality is planned for future releases
