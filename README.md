# Cipher

Simple terminal app with which you can code and decode messages in Rot13/Rot47.

## Features

- Read and save messages from the *.json files
- Create new messages from within the program.
- Encode and decode messages in Rot13 and Rot47
- Show messages stored in program memory

## Installation

1. Clone the repository:
```bash
git clone https://github.com/LukaszFraczek/Cipher
cd Cipher
```

2. Set up a Python virtual environment (optional but recommended):
```bash
# On Windows
python -m venv venv

# On macOS and Linux
python3 -m venv venv
```

3. Activate the virtual environment (if set up):
```bash
# On Windows
venv\Scripts\activate

# On macOS and Linux
source venv/bin/activate
```

4. Install the project dependencies:
```bash
pip install -r requirements.txt
```

## Launching the app

1. Run the app from root folderr:
```bash
python app\main.py
```

## How do I use it?

As for most console apps, user inputs and corresponding options are clearly described in the console after launching the app.
For the purpose of saving and loading files with messages, the app folder is treated as root folder.

![obraz](https://github.com/LukaszFraczek/Cipher/assets/30197518/97b7199f-ddd3-4217-89d5-67322ea3bd03)
