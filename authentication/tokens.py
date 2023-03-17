from django.contrib.auth.tokens import PasswordResetTokenGenerator
# import six
from six import text_type

from uuid import UUID


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.username) + text_type(user.uid) +
            text_type(timestamp)
        )


account_activation_token = TokenGenerator()


class CheckUUID:

    def __init__(self, uuid, version=4):
        self.uuid = uuid
        self.version = version

    def is_valid_uuid(self, uuid_to_test: str):
        """
            Check if uuid_to_test is a valid UUID.

            Parameters
            ----------
            uuid_to_test : str
            version : {1, 2, 3, 4}

            Returns
            -------
            `True` if uuid_to_test is a valid UUID, otherwise `False`.

            Examples
            --------
            >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
            True
            >>> is_valid_uuid('c9bf9e58')
            False
        """
        try:
            uuid_obj = UUID(uuid_to_test, version=self.version)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test
