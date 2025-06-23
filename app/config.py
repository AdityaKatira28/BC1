from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    frontend_url: str = "*"
    model_path: str
    log_level: str = "INFO"

    @property
    def frontend_url_list(self) -> List[str]:
        if self.frontend_url == "*":
            return ["*"]
        return [url.strip() for url in self.frontend_url.split(',')]

    class Config:
        env_file = ".env"
        protected_namespaces = ('settings_',)

settings = Settings()