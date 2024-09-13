# Automated Screenshot Capture and PDF Generation

This project provides a tool for automated screenshot capture, key simulation, and PDF generation. It's designed to streamline the process of capturing multiple screenshots and compiling them into a single PDF document.

## Features

- Capture full-screen or region-of-interest screenshots
- Simulate key presses between screenshots
- Automatically save screenshots to a specified directory
- Compile all captured screenshots into a single PDF file
- Configurable delay times and repeat counts

## Installation

1. Clone this repository

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the main script with the following command-line arguments:

```
python main.py -r <repeat_count> -s <save_directory> -f
```

- `-c <repeat_count>`: Number of screenshots to capture (required)
- `-d <save_directory>`: Directory to save screenshots and PDF (required)
- `-r`: Optional flag to capture a region of interest instead of full screen

Note:

- If the `-r` flag is not provided, the script will capture screenshots in full-screen mode.
- Directory to save must be provided via `-d` flag.


Example:
```
python main.py -c 5 -d ./screenshots -f
```

This command will capture 5 screenshots in full-screen mode and save them in the `./screenshots` directory.

## Configuration

Key press simulation and delay times can be configured in the `resources/single_key.json` file.

## Testing

Run the test suite with:
```
python -m unittest discover tests
```

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for more details.