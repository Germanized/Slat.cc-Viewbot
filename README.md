# Slat.cc Destroyer

Slat.cc Destroyer is a tool for simulating views on a specified URL. The tool uses Selenium and CustomTkinter to provide a graphical interface for easy usage.

## Requirements

- Python 3.x
- `chromedriver_autoinstaller`
- `undetected_chromedriver`
- `requests`
- `colorama`
- `customtkinter`
- `selenium`

You can install the required packages using pip:

pip install chromedriver_autoinstaller undetected_chromedriver requests colorama customtkinter selenium

## Files Needed

- `proxy.txt` - A text file containing a list of proxies.
- `mainobf.py` - The script file for the view bot application.

## Usage

1. **Setup Proxies:**
   Ensure that `proxy.txt` contains a list of proxies in the following format:
   http://proxy1:port

   
3. **Using the GUI:**
- **Enter the Target URL:** Input the URL where you want to simulate views.
- **Start View Botting:** Click the "Start View Botting" button and enter the number of views you want to simulate.
- **Check Proxies:** Click the "Check Proxies" button to test the proxies and save working ones to `workingproxy.txt`.
- **Exit:** Click the "Exit" button to close the application.

## Notes

- Ensure that you have Google Chrome installed and accessible via `C:\Program Files\Google\Chrome\Application\chrome.exe`.
- The application uses `chromedriver_autoinstaller` to manage the ChromeDriver binary.
- Errors and status updates will be shown in the GUI and printed to the console.

## License/Credits

This was made by Germanized
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
