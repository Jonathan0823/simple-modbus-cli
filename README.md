# Simple Modbus CLI Tool

Lightweight tool for reading/writing Modbus TCP holding registers via terminal input. Suitable for quick testing without a Streamlit dashboard.

## Project Structure
```
simple_modbus_cli/
├── main.py            # Interactive script
├── requirements.txt   # Dependencies (pymodbus)
└── README.md          # Documentation
```

## How to Use
1. (Optional) Create a new virtualenv.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```
4. Follow the prompts:
   - Enter device IP (default `127.0.0.1`).
   - Enter port (default `502`).
   - Enter Slave ID (default `1`).
   - Choose action `r` (read) or `w` (write), then enter register address & value.
   - Type `q` to exit and close the connection.

## Notes
- The script uses `read_holding_registers` and `write_register`, so make sure the device supports holding registers at the addresses you enter.
- Connection timeout is set to 3 seconds; adjust in `main.py` if your network is slow.
- If an error occurs, the terminal message will indicate whether it's a connection issue, write issue, or device response issue.
