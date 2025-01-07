from fastapi import HTTPException, status


class APIError:
    NOT_FOUND = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Resource not found",
    )

    UNAUTHORIZED = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )

    FORBIDDEN = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions",
    )

    @staticmethod
    def not_found(resource: str):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found",
        )

    @staticmethod
    def already_exists(resource: str):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{resource} already exists",
        )
