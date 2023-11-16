from settings import Settings


settings = Settings()


def get_cors_address():
    return [data for data in settings.cors_data.split(',')]
