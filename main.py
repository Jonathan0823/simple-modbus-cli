"""Simple interactive Modbus TCP client.

Usage:
    python main.py

The script will prompt for connection info (IP, port, slave ID)
then let you read/write holding registers via simple text inputs.
"""

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException


def prompt(message, default=None, cast=str):
    """Prompt user with optional default and casting."""
    suffix = f" [{default}]" if default is not None else ""
    raw = input(f"{message}{suffix}: ").strip()
    if not raw:
        if default is None:
            raise ValueError("Input tidak boleh kosong")
        raw = default
    try:
        return cast(raw)
    except Exception as exc:  # pragma: no cover - interactive helper
        print(f"⚠️  Nilai tidak valid ({exc}). Coba lagi.")
        return prompt(message, default, cast)


def read_registers(client, slave_id):
    address = prompt("Alamat register (holding)", cast=int)
    count = prompt("Jumlah register yang dibaca", default=1, cast=int)
    try:
        response = client.read_holding_registers(address=address, count=count, slave=slave_id)
        if response.isError():
            print(f"❌ Gagal membaca register: {response}")
        else:
            print(f"✅ Data dari alamat {address} s/d {address + count - 1}: {response.registers}")
    except ModbusIOException as exc:
        print(f"❌ Modbus IO error saat membaca: {exc}")
    except Exception as exc:  # pragma: no cover - runtime safety
        print(f"❌ Error tak terduga saat membaca: {exc}")


def write_register(client, slave_id):
    address = prompt("Alamat register (holding)", cast=int)
    value = prompt("Nilai yang akan ditulis (0-65535)", cast=int)
    try:
        response = client.write_register(address=address, value=value, slave=slave_id)
        if response.isError():
            print(f"❌ Gagal menulis register: {response}")
        else:
            print(f"✅ Nilai {value} berhasil ditulis ke alamat {address}")
    except ModbusIOException as exc:
        print(f"❌ Modbus IO error saat menulis: {exc}")
    except Exception as exc:  # pragma: no cover - runtime safety
        print(f"❌ Error tak terduga saat menulis: {exc}")


def main():
    print("==============================")
    print(" Simple Modbus TCP CLI Tool")
    print("==============================\n")

    ip = prompt("IP address perangkat", default="127.0.0.1")
    port = prompt("Port", default=502, cast=int)
    slave_id = prompt("Slave ID", default=1, cast=int)

    client = ModbusTcpClient(ip, port=port, timeout=3)

    print("\n🔌 Mencoba terhubung...")
    if not client.connect():
        print("❌ Tidak bisa terhubung. Periksa IP/port/perangkat.")
        return
    print("✅ Terhubung! Gunakan menu berikut.\n")

    try:
        while True:
            action = input("Pilih aksi - [r]ead, [w]rite, [q]uit: ").strip().lower()
            if action in {"q", "quit"}:
                print("👋 Keluar dari aplikasi.")
                break
            if action in {"r", "read"}:
                read_registers(client, slave_id)
            elif action in {"w", "write"}:
                write_register(client, slave_id)
            else:
                print("⚠️  Pilihan tidak dikenali.")
    finally:
        if client.is_socket_open():
            client.close()
            print("🔌 Koneksi ditutup.")


if __name__ == "__main__":
    main()
