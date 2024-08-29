class LoginFailedException(Exception):
    def __init__(self):
        super().__init__('login failed')
        