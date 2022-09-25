from pathlib import Path
import shutil
from subprocess import check_call
from typing import Callable, Dict

from PIL import Image

from .errors import GifFileSizeExceed, GifUnsupportedStickerFmt

DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512


def _png_gif_prepare(image: Image.Image):
    # NOTE: Copy from python-lottie by mattbas
    # https://gitlab.com/mattbas/python-lottie/-/blob/master/lib/lottie/exporters/gif.py#L10
    if image.mode not in ["RGBA", "RGBa"]:
        image = image.convert("RGBA")
    alpha = image.getchannel("A")
    image = image.convert("RGB").convert(
        'P', palette=Image.ADAPTIVE, colors=255)
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    image.paste(255, mask=mask)
    return image


def _convert_static_to_gif_once(image: Image.Image, dest_file_path: Path):
    image.save(str(dest_file_path), format='GIF', transparency=255)


def _convert_static_to_gif(src_file_path: Path, dest_file_path: Path,
                           gif_size_limit: int):
    image = Image.open(src_file_path)
    image = _png_gif_prepare(image)
    _convert_static_to_gif_once(image, dest_file_path)

    expected_compress_ratio = \
        gif_size_limit / dest_file_path.stat().st_size * 0.8
    if expected_compress_ratio < 1:
        ratio = expected_compress_ratio**0.5
        image = image.resize((int(image.width * ratio),
                              int(image.height * ratio)))
        _convert_static_to_gif_once(image, dest_file_path)


def _convert_tgs_to_gif_once(src_file_path: Path, dest_file_path: Path,
                             width: int, height: int, fps: int, quality: int):
    tmp_png_dir = src_file_path.parent / src_file_path.stem
    shutil.rmtree(str(tmp_png_dir), ignore_errors=True)
    tmp_png_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(str(src_file_path), str(tmp_png_dir / 'tmp.tgs'))

    check_call([
        'docker',
        'run',
        '-e',
        'FORMAT=gif',
        '-e',
        'WIDTH={}'.format(width),
        '-e',
        'HEIGHT={}'.format(height),
        '-e',
        'FPS={}'.format(fps),
        '-e',
        'QUALITY={}'.format(quality),
        '--rm',
        '-v',
        "{}:/source".format(tmp_png_dir),
        'edasriyan/tgs-to-gif',
    ])

    shutil.copy(str(tmp_png_dir / 'tmp.tgs.gif'), str(dest_file_path))


def _convert_tgs_to_gif(src_file_path: Path, dest_file_path: Path,
                        gif_size_limit: int):
    _convert_tgs_to_gif_once(
        src_file_path,
        dest_file_path,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
        fps=50,
        quality=90)
    if dest_file_path.stat().st_size <= gif_size_limit:
        return

    # First reduce quality & fps to save size
    _convert_tgs_to_gif_once(
        src_file_path,
        dest_file_path,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
        fps=30,
        quality=60)
    if dest_file_path.stat().st_size <= gif_size_limit:
        return

    # Scale to save size
    expected_compress_ratio = \
        gif_size_limit / dest_file_path.stat().st_size * 0.8
    _convert_tgs_to_gif_once(
        src_file_path,
        dest_file_path,
        width=int(DEFAULT_WIDTH * expected_compress_ratio),
        height=int(DEFAULT_HEIGHT * expected_compress_ratio),
        fps=30,
        quality=60)


def _convert_webm_to_gif_once(src_file_path: Path,
                              dest_file_path: Path,
                              scale: float = 1.0):
    cmd = [
        'ffmpeg',
        '-i',
        str(src_file_path),
    ]
    if scale != 1.0:
        cmd += [
            '-vf',
            'scale=w=trunc(iw*{}/2)*2:h=-1'.format(scale),
        ]
    cmd += [
        '-loop',
        '0',
        '-y',
        str(dest_file_path),
    ]
    check_call(cmd)


def _convert_webm_to_gif(src_file_path: Path, dest_file_path: Path,
                         gif_size_limit: int):
    _convert_webm_to_gif_once(src_file_path, dest_file_path)
    expected_compress_ratio = \
        gif_size_limit / dest_file_path.stat().st_size * 0.7
    if expected_compress_ratio < 1:
        _convert_webm_to_gif_once(
            src_file_path, dest_file_path, scale=expected_compress_ratio**0.5)


_CONVERTED_DISPATCHER: Dict[str, Callable[[Path, Path, int], None]] = {
    '.webp': _convert_static_to_gif,
    '.png': _convert_static_to_gif,
    '.tgs': _convert_tgs_to_gif,
    '.webm': _convert_webm_to_gif,
}


def convert_sticker_to_gif(src_file_path: Path, dest_file_path: Path,
                           gif_size_limit: int):
    """Convert Telegram sticker file to GIF with a file size limit

    Args:
        src_file_path (Path): The source sticker path. Supported formats: webp, png, tgs, webm
        dest_file_path (Path): The output gif file path.
        gif_size_limit (int): The output gif file size limit in bytes.
    """
    internal_convertor = _CONVERTED_DISPATCHER.get(src_file_path.suffix)
    if not internal_convertor:
        raise GifUnsupportedStickerFmt
    internal_convertor(src_file_path, dest_file_path, gif_size_limit)
    if dest_file_path.stat().st_size > gif_size_limit:
        raise GifFileSizeExceed
