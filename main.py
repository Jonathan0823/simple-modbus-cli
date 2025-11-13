"""Entry point for the Simple Modbus TCP CLI tool."""

from modbus_cli import ModbusCLIApp, PromptService


def main() -> None:
    prompt_service = PromptService()
    app = ModbusCLIApp(prompt_service)
    app.run()


if __name__ == "__main__":
    main()
