class FileManage:

    def __init__(self, file_path: str) -> None:
        """
        Initializes FileMange with specified file path.

        Args:
            file_path (str): The file path.
        """
        self.file_path = file_path
        with open(self.file_path, "w") as file:
            file.write("")

    def write_file(self, data: str) -> None:
        """
        Writes data to the file.

        Args:
            data (str): The data to write.
        """
        with open(self.file_path, "a") as file:
            file.write(f"{data}\n")

    def read_last_line(self) -> str:
        """
        Reads the last line of the file.

        Returns:
            str: The last line of the file, stripped of whitespace.
                 Returns an empty string if the file is empty.
        """
        with open(self.file_path, "r") as file:
            lines = file.readlines()
            if lines:
                return lines[-1].strip()
            return ""
