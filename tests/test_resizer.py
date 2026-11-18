import os
import pytest
from PIL import Image
from app.resizer import ImageResizer


@pytest.fixture
def sample_image(tmp_path):
    img_path = str(tmp_path / "test_input.png")
    img = Image.new("RGBA", (200, 100), color="red")
    img.save(img_path)
    return img_path


def test_calculate_dimensions_scale():
    w, h = ImageResizer.calculate_dimensions((200, 100), scale_percent=50)
    assert w == 100
    assert h == 50


def test_calculate_dimensions_keep_aspect():
    w, h = ImageResizer.calculate_dimensions((200, 100), target_width=100, target_height=100, keep_aspect_ratio=True)
    assert w == 100
    assert h == 50


def test_calculate_dimensions_ignore_aspect():
    w, h = ImageResizer.calculate_dimensions((200, 100), target_width=100, target_height=100, keep_aspect_ratio=False)
    assert w == 100
    assert h == 100


def test_resize_single_image(sample_image, tmp_path):
    out_path = str(tmp_path / "output.jpg")
    res = ImageResizer.resize_image(
        input_path=sample_image,
        output_path=out_path,
        target_width=100,
        output_format="JPEG"
    )
    assert os.path.exists(res)
    with Image.open(res) as img:
        assert img.size == (100, 50)
        assert img.format == "JPEG"


def test_batch_resize(sample_image, tmp_path):
    out_dir = str(tmp_path / "batch_out")
    results = ImageResizer.batch_resize(
        file_paths=[sample_image],
        output_dir=out_dir,
        scale_percent=25,
        output_format="PNG"
    )
    assert len(results) == 1
    assert os.path.exists(results[0])
    with Image.open(results[0]) as img:
        assert img.size == (50, 25)
        assert img.format == "PNG"
