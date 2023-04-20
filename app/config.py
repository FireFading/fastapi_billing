from app.settings import JWTSettings, Settings

settings = Settings(_env_file=".env.example")
jwt_settings = JWTSettings(_env_file=".env.example")
