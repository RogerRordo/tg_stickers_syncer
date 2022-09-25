from enum import IntEnum
from typing import Optional


class ErrorCode(IntEnum):
    UNKNOWN = 0
    NO_FILE_NAME_ATTR_FOR_DOC = 1

    # Github
    GITHUB_UNKNOWN = 100
    GITHUB_BRANCH_EXIST = 101

    # GIF
    GIF_UNKNOWN = 200
    GIF_UNSUPPORTED_STICKER_FMT = 201
    GIF_FILE_SIZE_EXCEED = 202


class BaseError(Exception):
    error_code: ErrorCode = ErrorCode.UNKNOWN
    message: Optional[str] = None

    def get_message(self) -> str:
        if self.message is None:
            raise NotImplementedError
        return self.message

    def __init__(self, message=None):
        super().__init__()
        self.message = message or self.message

    def __str__(self):
        return str(self.get_message())


# ========================= Main =========================
class NoFileNameAttrForDocError(BaseError):
    error_code = ErrorCode.NO_FILE_NAME_ATTR_FOR_DOC
    message = 'No file name attr for document'


# ========================= Github =========================
class GithubBaseError(BaseError):
    error_code: ErrorCode = ErrorCode.GITHUB_UNKNOWN


class GithubBranchExistError(GithubBaseError):
    error_code = ErrorCode.GITHUB_BRANCH_EXIST
    message = 'Branch already exists'


# ========================= GIF =========================
class GifBaseError(BaseError):
    error_code: ErrorCode = ErrorCode.GIF_UNKNOWN


class GifUnsupportedStickerFmt(GifBaseError):
    error_code = ErrorCode.GIF_UNSUPPORTED_STICKER_FMT
    message = 'Unsupported sticker format'


class GifFileSizeExceed(GifBaseError):
    error_code = ErrorCode.GIF_FILE_SIZE_EXCEED
    message = 'File size exceeds limit'
