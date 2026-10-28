def importData(
    path: str = ""
) -> str:
    """Zwraca zawartosc pliku albo "" gdy pliku nie da się odczytac."""

    try:
        with open(path, mode="r", encoding="utf-8") as f:
            return f.read()
    except OSError:  # m.in. FileNotFoundError, PermissionError, IsADirectoryError
        return ""
