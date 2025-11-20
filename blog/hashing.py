import bcrypt


class Hash():
    @staticmethod
    def bcrypt(password: str) -> str:
        # Convert to bytes and handle length
        password_bytes = password.encode('utf-8')

        # Truncate to 72 bytes if necessary
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]

        # Generate salt and hash
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)

        # Return as string for storage
        return hashed_bytes.decode('utf-8')

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        # Convert both to bytes
        plain_bytes = plain_password.encode('utf-8')
        if len(plain_bytes) > 72:
            plain_bytes = plain_bytes[:72]

        hashed_bytes = hashed_password.encode('utf-8')

        # Verify the password
        return bcrypt.checkpw(plain_bytes, hashed_bytes)