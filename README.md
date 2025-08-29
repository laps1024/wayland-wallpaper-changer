# Wayland Wallpaper Changer

Simple, lightweight Python script to shuffle wallpapers on your desktop. Powered by swww, fully compatible with Wayland.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/laps1024/wayland-wallpaper-changer
cd wayland-wallpaper-changer
```

Install the required dependencies:

**Arch Linux**

```bash
sudo pacman -S swww
```

**Fedora**

```bash
sudo dnf install swww
```

**Ubuntu / Debian**

```bash
sudo apt install swww
```

---

## Usage

Run the script with your desired time interval and wallpaper directory:

```bash
python3 main.py --time <time in minutes> --path <path to directory>
```

**Example:**

```bash
python3 main.py --time 30m --path ~/Pictures/Wallpapers
```

---

## Arguments

* `-t, --time` — Interval for changing wallpapers (default: `30m`)
* `-p, --path` — Path to the directory containing wallpapers

---

## Notes

* Make sure `swww-daemon` is installed and running.
* The script requires **at least 2 images** in the specified folder to shuffle properly.
* Supports common image formats: `.png`, `.jpg`, `.jpeg`.
