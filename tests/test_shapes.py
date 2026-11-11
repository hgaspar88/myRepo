import pytest
from geometry.shapes import circle_area, rectangle_area, triangle_area

def test_circle_area_positive_radius():
    assert circle_area(1.0) == pytest.approx(3.141592653589793)

def test_circle_area_zero_radius():
    assert circle_area(0.0) == 0.0

def test_circle_area_negative_radius():
    with pytest.raises(ValueError, match="Input must be non-negative"):
        circle_area(-1.0)

def test_rectangle_area_positive_dimensions():
    assert rectangle_area(2.0, 3.0) == 6.0

def test_rectangle_area_width_zero():
    assert rectangle_area(0.0, 5.0) == 0.0

def test_rectangle_area_height_zero():
    assert rectangle_area(4.0, 0.0) == 0.0

def test_rectangle_area_negative_width():
    with pytest.raises(ValueError, match="Input must be non-negative"):
        rectangle_area(-2.0, 3.0)

def test_rectangle_area_negative_height():
    with pytest.raises(ValueError, match="Input must be non-negative"):
        rectangle_area(2.0, -3.0)

def test_triangle_area_positive_base_height():
    assert triangle_area(2.0, 4.0) == 4.0

def test_triangle_area_base_zero():
    assert triangle_area(0.0, 5.0) == 0.0

def test_triangle_area_height_zero():
    assert triangle_area(6.0, 0.0) == 0.0

def test_triangle_area_negative_base():
    with pytest.raises(ValueError, match="Input must be non-negative"):
        triangle_area(-2.0, 3.0)

def test_triangle_area_negative_height():
    with pytest.raises(ValueError, match="Input must be non-negative"):
        triangle_area(2.0, -3.0)