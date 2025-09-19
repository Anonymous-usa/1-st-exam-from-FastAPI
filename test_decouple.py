from decouple import config

# Try to load variables from .env file
secret = config("secret", default="default_secret_key")
algorithm = config("algorithm", default="HS256")

print(f"JWT_SECRET: {secret}")
print(f"JWT_ALGORITHM: {algorithm}")
