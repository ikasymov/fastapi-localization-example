from typing import List

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import BaseSettings, BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import (
    EmailStr,
)

from fastapi_localization import (
    SystemLocalizationMiddleware,
    http_exception_handler,
    validation_exception_handler,
    LocalizationRoute,
    TranslatableStringField,
    TranslateJsonResponse,
)
from fastapi_localization import lazy_gettext as _


class Settings(BaseSettings):
    localization_dir: str = 'locales'
    localization_domain: str = 'base'


settings = Settings()
app = FastAPI()

# register localization middleware
localization_middleware = SystemLocalizationMiddleware(
        domain=settings.localization_domain,
        translation_dir=settings.localization_dir,
)
app.add_middleware(BaseHTTPMiddleware, dispatch=localization_middleware)


# register error handlers for localization errors
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


app.router.route_class = LocalizationRoute


class LanguageTranslatableSchema(BaseModel):
    code: str
    title: TranslatableStringField


@app.get(
    '/language',
    response_class=TranslateJsonResponse,
    response_model=List[LanguageTranslatableSchema])
async def languages():
    return [{'code': 'ru', 'title': 'Russia'},
            {'code': 'en', 'title': 'English'}]


@app.get(
    '/country',
    response_class=TranslateJsonResponse)
async def countries():
    return [{'code': 'ru', 'title': _('Russia')},
            {'code': 'us', 'title': 'USA'}]


class InputSchema(BaseModel):
    email = EmailStr()


@app.post(
    '/input',
    response_class=TranslateJsonResponse)
async def countries(value: InputSchema):
    return value
