from enum import Enum


class SettingsKey(Enum):
    JWT_AUTH_TOKEN_DURATION = "JWT lifetime for users authenticated by SSO (seconds)"
    JWT_REFRESH_TOKEN_DURATION = "JWT refresh token lifetime (seconds)"

    SAML_METADATA = "SAML metadata path - URL or path inside workdir"
    SAML_HOST = "Application hostname as configured on IdP"
    SAML_ENTITY_ID = "Application entity ID as configured on IdP"
    SAML_DEFAULT_NEXT_URL = "Default URL to redirect to after successful authentication"

    NOT_SSO_AUTH_COMPANIES = "List of companies without SSO authentication"
