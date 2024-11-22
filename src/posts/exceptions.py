"""
HTTP исключения.
"""

from typing import Any, Dict, Union

from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self,
                 status_code: int = status.HTTP_404_NOT_FOUND,
                 detail: Any = None,
                 headers: Union[Dict[str, str], None] = None) -> None:
        super().__init__(status_code, detail, headers)


class CategoryDoesNotExistException(HTTPException):
    MESSAGE = "The selected category does not exist."

    def __init__(self,
                 status_code: int = status.HTTP_404_NOT_FOUND,
                 detail: Any = MESSAGE,
                 headers: Union[Dict[str, str], None] = None) -> None:
        super().__init__(status_code, detail, headers)


class FobidenToPostException(HTTPException):
    MESSAGE = "It is forbidden to change someone else's content."

    def __init__(self,
                 status_code: int = status.HTTP_403_FORBIDDEN,
                 detail: Any = MESSAGE,
                 headers: Union[Dict[str, str], None] = None) -> None:
        super().__init__(status_code, detail, headers)


class EmptyValueException(HTTPException):
    def __init__(self,
                 status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
                 detail: Any = None,
                 headers: Union[Dict[str, str], None] = None) -> None:

        super().__init__(status_code, detail, headers)
        self.detail = "The field '{field}' value cannot be empty.".format(
            field=detail)


class NotEnoughRightsException(HTTPException):
    MESSAGE = "You do not have sufficient rights to perform this operation."

    def __init__(self,
                 status_code: int = status.HTTP_403_FORBIDDEN,
                 detail: Any = MESSAGE,
                 headers: Union[Dict[str, str], None] = None) -> None:
        super().__init__(status_code, detail, headers)
