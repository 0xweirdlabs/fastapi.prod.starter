"""
PKCE (Proof Key for Code Exchange) utilities for OAuth 2.0 flow.
"""
import base64
import hashlib
import secrets
import json
from typing import Dict, Tuple

def generate_pkce_pair() -> Tuple[str, str]:
    """
    Generate a code verifier and code challenge pair for PKCE.
    
    Returns:
        Tuple[str, str]: A tuple containing (code_verifier, code_challenge)
    """
    # Generate a secure random string for the code verifier
    code_verifier = secrets.token_urlsafe(64)
    
    # Create code challenge by hashing the verifier with SHA-256
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').rstrip('=')
    
    return code_verifier, code_challenge

def generate_state_with_verifier(code_verifier: str) -> str:
    """
    Generate a state parameter that includes the code verifier.
    
    Args:
        code_verifier: The code verifier to include in the state
        
    Returns:
        str: A base64-encoded state parameter containing the verifier
    """
    # Create a state object with the verifier and a nonce for security
    state_obj = {
        "verifier": code_verifier,
        "nonce": secrets.token_hex(8)
    }
    
    # Encode the state as JSON and then base64
    state_json = json.dumps(state_obj)
    state = base64.urlsafe_b64encode(state_json.encode('utf-8')).decode('utf-8')
    
    return state

def extract_verifier_from_state(state: str) -> str:
    """
    Extract the code verifier from a state parameter.
    
    Args:
        state: The base64-encoded state parameter
        
    Returns:
        str: The code verifier
        
    Raises:
        ValueError: If the state is invalid or doesn't contain a verifier
    """
    try:
        # Decode the state from base64 to JSON
        state_json = base64.urlsafe_b64decode(state.encode('utf-8')).decode('utf-8')
        state_obj = json.loads(state_json)
        
        # Extract the verifier
        if "verifier" not in state_obj:
            raise ValueError("State does not contain a verifier")
        
        return state_obj["verifier"]
    except Exception as e:
        raise ValueError(f"Invalid state parameter: {str(e)}")
