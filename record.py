import subprocess
import os
import time
from utils.to_html import xml_to_html
def record_ui(output_dir="recordings", app="yt", interval=5):
    """
    Repeatedly record XML and screenshot from Android Emulator.

    Args:
        output_dir (str): Directory to save the XML and screenshots.
        interval (int): Time in seconds between captures.
    """

    # Ensure adb is available
    try:
        subprocess.run(["adb", "devices"], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("Error: adb is not available. Please install or add it to PATH.")
        return

    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)

    count = 17
    print(f"Starting UI recording... Output in '{output_dir}' every {interval} seconds.")
    try:
        while True:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            count += 1

            # 1. Dump XML
            xml_path = os.path.join(output_dir, f"{app}_{count}.xml")
            with open(xml_path, "wb") as f:
                xml_data = subprocess.run(
                    ["adb", "exec-out", "uiautomator", "dump", "/dev/tty"],
                    stdout=subprocess.PIPE
                ).stdout
                # Sometimes there are extra stdout messages, keep only xml part
                start = xml_data.find(b'<?xml')
                end = xml_data.find(b'</hierarchy>') + len(b'</hierarchy>')
                if start != -1 and end != -1:
                    f.write(xml_data[start:end])
                else:
                    print(f"Warning: Failed to parse XML at {timestamp}, snapshot {count}.")

            # 2. Take Screenshot
            screenshot_path = os.path.join(output_dir, f"{app}_{count}.png")
            with open(screenshot_path, "wb") as f:
                screenshot_data = subprocess.run(
                    ["adb", "exec-out", "screencap", "-p"],
                    stdout=subprocess.PIPE
                ).stdout
                f.write(screenshot_data)

            
            # 3. Convert XML to HTML
            html_path = os.path.join(output_dir, f"{app}_{count}.html")
            with open(html_path, "w", encoding="utf-8") as f:
                xml_string = open(xml_path, 'r', encoding='utf-8').read()
                html_result = xml_to_html(xml_string)
                f.write(html_result)
            
            # print(f"Captured {count}: {screenshot_path}")
            print(f"Captured {count}: {xml_path}, {screenshot_path}, {html_path}")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nStopped recording.")

if __name__ == "__main__":
    app_name = "random" # Change this to your desired app name
    outputdir = "/Users/rui/Documents/GitHub/MobileSafety/random_ui_recordings" # Change this to your desired output directory
    record_ui(output_dir=outputdir, app=app_name, interval=5)
