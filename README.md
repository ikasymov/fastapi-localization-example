# fastapi_localization-example

**fastapi_localization-example** - simple rest application with language localization wia Accept-Language headers.

Run
```shell script
$ uvicorn app.main:app --reload
```

Example

```python
class LanguageTranslatableSchema(BaseModel):
    code: str
    title: TranslatableStringField


@app.get(
    '/language',
    response_class=TranslateJsonResponse,
    response_model=List[LanguageTranslatableSchema])
def languages():
    return [{'code': 'ru', 'title': 'Russia'},
            {'code': 'en', 'title': 'English'}]
```
```shell script
$ curl --location --request GET 'http://127.0.0.1:8000/language' \
--header 'Accept-Language: ru'

[{"code":"ru","title":"Русский"},{"code":"en","title":"Английский"}]
```

manual partial translation
```python
@app.get(
    '/country',
    response_class=TranslateJsonResponse)
def countries():
    return [{'code': 'ru', 'title': _('Russia')},
            {'code': 'us', 'title': 'USA'}]
```

```shell script
$ curl --location --request GET 'http://127.0.0.1:8000/country' \
--header 'Accept-Language: ru'

[{"code":"ru","title":"Русский"},{"code":"us","title":"USA"}]
```

error validation 

```python
class InputSchema(BaseModel):
    email = EmailStr()


@app.post(
    '/input',
    response_class=TranslateJsonResponse)
def countries(value: InputSchema):
    return value
```
```shell script
$ curl --location --request POST 'http://127.0.0.1:8000/input' \
--header 'Accept-Language: ru' \
--header 'Content-Type: application/json' \
--data-raw '{"email": "invalid_email"}'

{
    "detail": [
        {
            "loc": [
                "body",
                "email"
            ],
            "msg": "значение не является действительным адресом электронной почты",
            "type": "value_error.email"
        }
    ]
}
```

