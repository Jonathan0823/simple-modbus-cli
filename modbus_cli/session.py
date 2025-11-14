"""Encapsulation of Modbus client operations."""

from __future__ import annotations

from typing import Type

from pymodbus.client import ModbusTcpClient
from pymodbus.framer import FramerType


class ModbusSession:
    """Encapsulates Modbus client lifecycle and basic operations."""

    def __init__(
        self,
        host: str,
        port: int,
        slave_id: int,
        timeout: int = 3,
        client_cls: Type[ModbusTcpClient] = ModbusTcpClient,
    ) -> None:
        self.host = host
        self.port = port
        self.slave_id = slave_id
        self.timeout = timeout
        self._client = client_cls(
            host, port=port, timeout=timeout, framer=FramerType.RTU
        )

    def connect(self) -> bool:
        return self._client.connect()

    def read_holding_registers(self, address: int, count: int):
        return self._client.read_holding_registers(
            address=address, count=count, slave=self.slave_id
        )

    def write_holding_register(self, address: int, value: int):
        return self._client.write_register(
            address=address, value=value, slave=self.slave_id
        )

    def is_connected(self) -> bool:
        return bool(self._client and self._client.is_socket_open())

    def close(self) -> None:
        if self.is_connected():
            self._client.close()
