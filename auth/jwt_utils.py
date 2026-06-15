from datetime import datetime, timedelta, timezone
import jwt

with open("private.pem", "r") as f:
    PRIVATE_KEY = f.read()

ALGORITHM = "RS256"
ISSUER = "auth-service"

# Why RS256?
# Auth service holds private key
# All other services get public key
# Even if backend is compromised → attacker cannot mint tokens

def create_token(payload):
    payload = {
        **payload,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }

    token = jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)
    return token
