import os
from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):

    DATABASE_SERVICE_NAME: str = os.getenv('DATABASE_SERVICE_NAME','db')
    DATABASE_ENGINE: str = os.getenv('DATABASE_ENGINE','postgresql')
    DATABASE_NAME: str = os.getenv('DATABASE_NAME')
    DATABASE_USER: str = os.getenv('DATABASE_USER')
    DATABASE_PASSWORD: str = os.getenv('DATABASE_PASSWORD')
    DB_SERVICE_HOST: str = os.getenv('DB_SERVICE_HOST')
    DB_SERVICE_PORT: str = os.getenv('DB_SERVICE_PORT')

    OIDC_RP_PROVIDER_URL: str = os.getenv('OIDC_RP_PROVIDER_URL')
    OIDC_RP_PROVIDER_REALM: str = os.getenv('OIDC_RP_PROVIDER_REALM')
    OIDC_RP_CLIENT_ID : str= os.getenv('OIDC_RP_CLIENT_ID')
    OIDC_RP_CLIENT_SECRET: str = os.getenv('OIDC_RP_CLIENT_SECRET')
    OIDC_RP_KC_IDP_HINT: str = os.getenv('OIDC_RP_KC_IDP_HINT')

    FRONTEND_HOST_URL: str = os.getenv('FRONTEND_HOST_URL','http://localhost:8081')
    DEFAULT_BASE_URL: str = os.getenv('DEFAULT_BASE_URL' ,'/court-interpreter-scheduling')
    URL_SCHEME: str = os.getenv('URL_SCHEME' ,'http')    
    APP_RUN_IN_DOCKER: str = os.getenv('APP_RUN_IN_DOCKER', 'False')
    
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY','5e094faa6ca25ahc81816')
    DATA_SECURITY_KEY: str = os.getenv('DATA_SECURITY_KEY')

    PDF_SERVICE_URL: str = os.getenv('PDF_SERVICE_URL') 
    
    # # JC Interface
    JC_INTERFACE_API_LOCATION_URL: str = os.getenv('JC_INTERFACE_API_LOCATION_URL')
    JC_INTERFACE_API_USERNAME: str = os.getenv('JC_INTERFACE_API_USERNAME')
    JC_INTERFACE_API_PASSWORD: str = os.getenv('JC_INTERFACE_API_PASSWORD')

    # # Efiling Hub
    EFILING_HUB_API_BASE_URL: str = os.getenv('EFILING_HUB_API_BASE_URL')
    EFILING_HUB_KEYCLOAK_CLIENT_ID: str = os.getenv('EFILING_HUB_KEYCLOAK_CLIENT_ID')
    EFILING_HUB_KEYCLOAK_BASE_URL: str = os.getenv('EFILING_HUB_KEYCLOAK_BASE_URL')
    EFILING_HUB_KEYCLOAK_SECRET: str = os.getenv('EFILING_HUB_KEYCLOAK_SECRET')
    EFILING_HUB_KEYCLOAK_REALM: str = os.getenv('EFILING_HUB_KEYCLOAK_REALM')

    # # API
    API_PREFIX: str = os.getenv('API_PREFIX', '/api/v1')
    API_VERSION: str = '0.1.0'
    API_TITLE: str = 'Court Interpreter System API'
    API_DESCRIPTION: str = API_TITLE
   
    # # Geo coordinate calls
    GOOGLE_MAP_URL: str = os.getenv('GOOGLE_MAP_URL')
    OPENROAD_MAP_URL: str = os.getenv('OPENROAD_MAP_URL')

    # # cors
    CORS_ORIGIN: List[str] = str(os.getenv('CORS_ORIGIN', '*')).split(',')    
    # # # LOCAL DEV: CORS_ORIGIN=http://localhost:8000,http://0.0.0.0:8000
    # # # TESTING: CORS_ORIGIN=https://www.???
    # # # PRODUCTION: CORS_ORIGIN=https://www.???

    # # CHES Email service
    CHES_AUTH_URL: str = os.getenv('CHES_AUTH_URL')
    CHES_EMAIL_URL: str = os.getenv('CHES_EMAIL_URL')
    EMAIL_SERVICE_CLIENT_ID: str = os.getenv('EMAIL_SERVICE_CLIENT_ID')
    EMAIL_SERVICE_CLIENT_SECRET: str = os.getenv('EMAIL_SERVICE_CLIENT_SECRET')
    RECIPIENT_EMAILS: str = os.getenv('RECIPIENT_EMAILS') 
    ADM_PRODUCTION_ENV: str = os.getenv('ADM_PRODUCTION_ENV','false')

    class Config:
        case_sensitive = True


settings = Settings()
