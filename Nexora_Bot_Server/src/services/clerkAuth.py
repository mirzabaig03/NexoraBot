from src.config.index import appConfig
from fastapi import Request, HTTPException
from src.services.userService import ensure_user_exists

from clerk_backend_api import Clerk
from clerk_backend_api.security.types import AuthenticateRequestOptions

import time

# Initialize SDK globally
clerk_sdk = Clerk(bearer_auth=appConfig["clerk_secret_key"])

# Simple in-memory cache: token -> (clerk_id, timestamp)
token_cache = {}
CACHE_TTL = 60  # seconds


def get_current_user_clerk_id(request: Request) -> str:
    start = time.time()

    try:
        auth_header = request.headers.get("Authorization")

        token = None
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            # Cache check
            if token in token_cache:
                cached_clerk_id, timestamp = token_cache[token]
                if time.time() - timestamp < CACHE_TTL:
                    #  Ensure user exists even on cache hit
                    ensure_user_exists(cached_clerk_id)
                    print(f"[Profiling] Clerk Auth (Cache Hit) took: {time.time() - start}s")
                    return cached_clerk_id
                else:
                    del token_cache[token]

        # Authenticate with Clerk
        request_state = clerk_sdk.authenticate_request(
            request,
            options=AuthenticateRequestOptions(
                authorized_parties=appConfig["domain"]
            ),
        )

        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="User is not signed in")

        clerk_id = request_state.payload.get("sub")

        if not clerk_id:
            raise HTTPException(status_code=401, detail="Clerk ID not found in token")

        # Ensure user exists in DB
        ensure_user_exists(clerk_id)

        # Update cache
        if token:
            token_cache[token] = (clerk_id, time.time())

        print(f"[Profiling] Clerk Auth (Miss) took: {time.time() - start}s")

        return clerk_id

    except HTTPException:
        raise

    except Exception as e:
        print(f"Clerk Auth Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Clerk SDK Failed. {str(e)}",
        )