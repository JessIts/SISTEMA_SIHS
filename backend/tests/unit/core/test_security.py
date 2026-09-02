from uuid import uuid4

import jwt
import pytest

from app.core.config import settings
from app.core.security import (
    create_access_token,
    decode_access_token,
)


def test_create_access_token():
    user_uuid = uuid4()

    token = create_access_token(str(user_uuid))

    assert isinstance(token, str)
    assert token


def test_decode_access_token():
    user_uuid = uuid4()

    token = create_access_token(str(user_uuid))
    payload = decode_access_token(token)

    assert payload["sub"] == str(user_uuid)
    assert "exp" in payload


def test_decode_access_token_invalid_token():
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token("token-invalido")


def test_decode_access_token_expired_token():
    user_uuid = uuid4()

    payload = {
        "sub": str(user_uuid),
        "exp": 0,
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token)