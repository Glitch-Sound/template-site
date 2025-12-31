from fastapi import HTTPException


def re_raise_as_internal_error(exc: Exception) -> None:
    """
    Preserve explicitly raised HTTPException instances while normalizing any
    unexpected error into a 500 response so individual endpoints do not have to
    repeat the same boilerplate.
    """
    if isinstance(exc, HTTPException):
        raise exc
    raise HTTPException(status_code=500, detail=str(exc)) from exc
