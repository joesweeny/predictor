class GRPCException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Code: {self.code} -> Message: {self.message}'
