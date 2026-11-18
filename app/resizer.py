import os
from typing import List, Tuple, Callable, Optional
from PIL import Image


class ImageResizer:
    """Handles core image resizing, aspect ratio calculation, and batch conversion."""

    SUPPORTED_FORMATS = {"JPEG", "PNG", "WEBP", "BMP"}

    @staticmethod
    def calculate_dimensions(
        original_size: Tuple[int, int],
        target_width: Optional[int] = None,
        target_height: Optional[int] = None,
        scale_percent: Optional[float] = None,
        keep_aspect_ratio: bool = True
    ) -> Tuple[int, int]:
        orig_w, orig_h = original_size
        if orig_w <= 0 or orig_h <= 0:
            raise ValueError("Original image dimensions must be positive.")

        if scale_percent is not None:
            scale = scale_percent / 100.0
            return max(1, int(orig_w * scale)), max(1, int(orig_h * scale))

        if target_width and target_height:
            if not keep_aspect_ratio:
                return max(1, target_width), max(1, target_height)
            ratio = min(target_width / orig_w, target_height / orig_h)
            return max(1, int(orig_w * ratio)), max(1, int(orig_h * ratio))

        if target_width:
            ratio = target_width / orig_w
            return max(1, target_width), max(1, int(orig_h * ratio))

        if target_height:
            ratio = target_height / orig_h
            return max(1, int(orig_w * ratio)), max(1, target_height)

        return orig_w, orig_h

    @classmethod
    def resize_image(
        cls,
        input_path: str,
        output_path: str,
        target_width: Optional[int] = None,
        target_height: Optional[int] = None,
        scale_percent: Optional[float] = None,
        keep_aspect_ratio: bool = True,
        output_format: Optional[str] = None,
        quality: int = 85
    ) -> str:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file does not exist: {input_path}")

        with Image.open(input_path) as img:
            orig_size = img.size
            new_size = cls.calculate_dimensions(
                orig_size, target_width, target_height, scale_percent, keep_aspect_ratio
            )

            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)

            fmt = (output_format or img.format or "JPEG").upper()
            if fmt == "JPG":
                fmt = "JPEG"

            if fmt == "JPEG" and resized_img.mode in ("RGBA", "P", "LA"):
                resized_img = resized_img.convert("RGB")

            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            save_kwargs = {}
            if fmt in ("JPEG", "WEBP"):
                save_kwargs["quality"] = max(1, min(100, quality))

            resized_img.save(output_path, format=fmt, **save_kwargs)
            return output_path

    @classmethod
    def batch_resize(
        cls,
        file_paths: List[str],
        output_dir: str,
        target_width: Optional[int] = None,
        target_height: Optional[int] = None,
        scale_percent: Optional[float] = None,
        keep_aspect_ratio: bool = True,
        output_format: Optional[str] = None,
        quality: int = 85,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> List[str]:
        results = []
        total = len(file_paths)
        for idx, path in enumerate(file_paths):
            filename = os.path.basename(path)
            name, ext = os.path.splitext(filename)

            fmt = output_format.upper() if output_format and output_format.upper() != "ORIGINAL" else None
            out_ext = f".{fmt.lower()}" if fmt else ext
            if out_ext.lower() == ".jpeg":
                out_ext = ".jpg"

            out_filename = f"{name}_resized{out_ext}"
            out_path = os.path.join(output_dir, out_filename)

            res_path = cls.resize_image(
                input_path=path,
                output_path=out_path,
                target_width=target_width,
                target_height=target_height,
                scale_percent=scale_percent,
                keep_aspect_ratio=keep_aspect_ratio,
                output_format=fmt,
                quality=quality
            )
            results.append(res_path)
            if progress_callback:
                progress_callback(idx + 1, total, res_path)

        return results
