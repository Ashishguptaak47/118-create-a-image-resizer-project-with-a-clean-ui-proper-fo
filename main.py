import sys
import argparse
from app.resizer import ImageResizer
from app.ui import ImageResizerApp


def run_cli(args):
    print(f"Processing {len(args.files)} images...")
    
    def progress_callback(current, total, path):
        print(f"[{current}/{total}] Resized -> {path}")

    try:
        results = ImageResizer.batch_resize(
            file_paths=args.files,
            output_dir=args.out,
            target_width=args.width,
            target_height=args.height,
            scale_percent=args.scale,
            keep_aspect_ratio=not args.no_aspect,
            output_format=args.format,
            quality=args.quality,
            progress_callback=progress_callback
        )
        print(f"Done! Resized {len(results)} image(s).")
    except Exception as e:
        print(f"Error during batch resize: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if "--cli" in sys.argv:
        parser = argparse.ArgumentParser(description="Batch Image Resizer CLI")
        parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
        parser.add_argument("--files", nargs="+", required=True, help="Paths to input images")
        parser.add_argument("--out", required=True, help="Output directory")
        parser.add_argument("--width", type=int, help="Target width in pixels")
        parser.add_argument("--height", type=int, help="Target height in pixels")
        parser.add_argument("--scale", type=float, help="Scale percentage (e.g. 50)")
        parser.add_argument("--no-aspect", action="store_true", help="Do not preserve aspect ratio")
        parser.add_argument("--format", choices=list(ImageResizer.SUPPORTED_FORMATS), help="Output format")
        parser.add_argument("--quality", type=int, default=85, help="JPEG/WEBP quality (1-100)")

        args = parser.parse_args()
        run_cli(args)
    else:
        app = ImageResizerApp()
        app.run()


if __name__ == "__main__":
    main()
