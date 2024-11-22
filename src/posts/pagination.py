from fastapi import Query
from fastapi_pagination import Page as Basepage
from fastapi_pagination.customization import UseParamsFields, CustomizedPage


Page = CustomizedPage[
    Basepage,
    UseParamsFields(
        size=Query(10, ge=1, le=50)
    )
]
