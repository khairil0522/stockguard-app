from app.core.security import create_access_token, decode_access_token


user_id = "12345678-1234-1234-1234-123456789abc"

# Generate JWT
token = create_access_token(user_id)

print("Token:")
print(token)

# Decode JWT
decoded_user_id = decode_access_token(token)

print("\nUser ID:")
print(decoded_user_id)