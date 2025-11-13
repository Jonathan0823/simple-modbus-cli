"""CLI orchestration for Modbus operations."""

from __future__ import annotations

from typing import Optional, Type

from pymodbus.exceptions import ModbusIOException

from .prompt import PromptService
from .session import ModbusSession


class ModbusCLIApp:
    """Handles CLI workflow, input loop, and user feedback."""

    def __init__(self, prompt_service: PromptService, session_cls: Type[ModbusSession] = ModbusSession) -> None:
        self.prompt_service = prompt_service
        self.session_cls = session_cls
        self.session: Optional[ModbusSession] = None

    def run(self) -> None:
        self._print_banner()
        connection = self._collect_connection_info()
        self.session = self.session_cls(**connection)

        print("\n🔌 Mencoba terhubung...")
        if not self.session.connect():
            print("❌ Tidak bisa terhubung. Periksa IP/port/perangkat.")
            return
        print("✅ Terhubung! Gunakan menu berikut.\n")

        try:
            self._main_loop()
        finally:
            self.session.close()
            print("🔌 Koneksi ditutup.")

    def _collect_connection_info(self) -> dict:
        ip = self.prompt_service.prompt("IP address perangkat", default="127.0.0.1")
        port = self.prompt_service.prompt("Port", default=502, cast=int)
        slave_id = self.prompt_service.prompt("Slave ID", default=1, cast=int)
        return {"host": ip, "port": port, "slave_id": slave_id}

    def _main_loop(self) -> None:
        while True:
            action = self.prompt_service.prompt("Pilih aksi - [r]ead, [w]rite, [q]uit", cast=str).strip().lower()
            if action in {"q", "quit"}:
                print("👋 Keluar dari aplikasi.")
                break
            if action in {"r", "read"}:
                self._handle_read()
            elif action in {"w", "write"}:
                self._handle_write()
            else:
                print("⚠️  Pilihan tidak dikenali.")

    def _handle_read(self) -> None:
        assert self.session is not None
        address = self.prompt_service.prompt("Alamat register (holding)", cast=int)
        count = self.prompt_service.prompt("Jumlah register yang dibaca", default=1, cast=int)
        try:
            response = self.session.read_holding_registers(address=address, count=count)
            if response.isError():
                print(f"❌ Gagal membaca register: {response}")
            else:
                print(f"✅ Data dari alamat {address} s/d {address + count - 1}: {response.registers}")
        except ModbusIOException as exc:
            print(f"❌ Modbus IO error saat membaca: {exc}")
        except Exception as exc:  # pragma: no cover - runtime safety
            print(f"❌ Error tak terduga saat membaca: {exc}")

    def _handle_write(self) -> None:
        assert self.session is not None
        address = self.prompt_service.prompt("Alamat register (holding)", cast=int)
        value = self.prompt_service.prompt("Nilai yang akan ditulis (0-65535)", cast=int)
        try:
            response = self.session.write_holding_register(address=address, value=value)
            if response.isError():
                print(f"❌ Gagal menulis register: {response}")
            else:
                print(f"✅ Nilai {value} berhasil ditulis ke alamat {address}")
        except ModbusIOException as exc:
            print(f"❌ Modbus IO error saat menulis: {exc}")
        except Exception as exc:  # pragma: no cover - runtime safety
            print(f"❌ Error tak terduga saat menulis: {exc}")

    @staticmethod
    def _print_banner() -> None:
        print("==============================")
        print(" Simple Modbus TCP CLI Tool")
        print("==============================\n")
