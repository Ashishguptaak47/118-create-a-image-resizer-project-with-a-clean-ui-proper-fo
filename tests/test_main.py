import sys
import pytest
from main import main
from PIL import Image


def test_cli_mode(tmp_path, monkeypatch):
    img_path = str(tmp_path / "cli_test.png")
    img = Image.new("RGB", (100, 100), color="blue")
    img.save(img_path)

    out_dir = str(tmp_path / "cli_out")

    test_args = [
        "main.py",
        "--cli",
        "--files", img_path,
        "--out", out_dir,
        "--scale", "50",
        "--format", "JPEG"
    ]
    monkeypatch.setattr(sys, "argv", test_args)

    main()
    
    expected_file = tmp_path / "cli_out" / "cli_test_resized.jpg"
    assert expected_file.exists()
