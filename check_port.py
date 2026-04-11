import socket


def check_port(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=3):
            return True
    except Exception:
        return False


print(check_port("127.0.0.1", 8080))
