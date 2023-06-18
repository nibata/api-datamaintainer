if __name__ == "__main__":
    print("#" * 30)
    print("CREATE .env FILE:")
    print("#" * 30)

    with open("./app/env/.env", "x") as f:
        SECRET_KEY = input("Enter Secret Key (default.- OK you didn't enter anything): ") or "OK you didn't enter anything"
        ADMIN_EMAIL = input("Enter Admin Email (default.- admin@admin.admin): ") or "admin@admin.admin"
        DEBUG = input("Debug Mode (True or False. default.- True): ") or "True"
        DB_DRIVER = input("Driver DB (default.- 'postgresql'): ") or "postgresql"
        DB_ASYNC_DRIVER = input("Driver async DataBase (default.- 'asyncpg'): ") or "asyncpg"
        DB_USER = input("DataBase User (default.- postgres): ") or "postgres"
        DB_PASS = input("DataBase Password (default.- postgrspw): ") or "postgrespw"
        DB_HOST = input("DataBase Host (default.- localhost): ") or "localhost"
        DB_PORT = input("DataBase Port (default.- 5432): ") or "5432"
        DB_DATABASE_NAME = input("Database name: ") or "FastAPI_DB"
        JWT_SECRET = input("JWT Secret (default .- please_please_update_me_please): ") or "please_please_update_me_please"
        JWT_ALGORITHM = input("JWT Algorithm (default.- HS256): ") or "HS256"
        USER_ADMIN = input("User Admin email for DataBase (default.- the same as Admin Email): ") or ADMIN_EMAIL
        PASS_ADMIN = input("User Admin password for DataBase (default.- admin): ") or "admin"
        SENTRY_DNS = input("Sentry DNS (only if you have one): ") or "''"

        f.write(f"SECRET_KEY={SECRET_KEY}\n")
        f.write(f"ADMIN_EMAIL={ADMIN_EMAIL}\n")
        f.write(f"DEBUG={DEBUG}\n")
        f.write(f"DB_DRIVER={DB_DRIVER}\n")
        f.write(f"DB_USER={DB_USER}\n")
        f.write(f"DB_PASS={DB_PASS}\n")
        f.write(f"DB_HOST={DB_HOST}\n")
        f.write(f"DB_PORT={DB_PORT}\n")
        f.write(f"DB_DATABASE_NAME={DB_DATABASE_NAME}\n")
        f.write(f"JWT_SECRET={JWT_SECRET}\n")
        f.write(f"JWT_ALGORITHM={JWT_ALGORITHM}\n")
        f.write(f"USER_ADMIN={USER_ADMIN}\n")
        f.write(f"PASS_ADMIN={PASS_ADMIN}\n")
        f.write(f"SENTRY_DNS={SENTRY_DNS}\n")
        f.write(f"DB_ASYNC_DRIVER={DB_ASYNC_DRIVER}\n")

        f.close()

    print("FINISH!")
    print("Edit file at: '/app/env/.env'")
