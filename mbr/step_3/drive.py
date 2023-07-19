class Drive:
    def __init__(self, filename: str, bps: int, size: int):
        self.filename = filename
        self.bps = bps
        self.size = size
        self.fd = None
        self.open()

    def open(self):
        self.fd = open(self.filename, "rb")
        self.fd.seek(0)

    def seek(self, pos: int):
        self.fd.seek(pos * self.bps)

    def read(self, pos: int, size: int = 1):
        self.seek(pos)
        return self.fd.read(size * self.bps)

    def close(self):
        self.fd.close()
