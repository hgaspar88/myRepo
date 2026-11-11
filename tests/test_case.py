import pytest
from text_utils.case import to_snake_case, to_camel_case

def test_to_snake_case():
    assert to_snake_case("HelloWorld") == "hello_world"
    assert to_snake_case("hello_world") == "hello_world"
    assert to_snake_case("") == ""
    assert to_snake_case("a") == "a"
    assert to_snake_case("XMLHttpRequest") == "xml_http_request"

    with pytest.raises(TypeError):
        to_snake_case(123)
    with pytest.raises(TypeError):
        to_snake_case(None)
    with pytest.raises(TypeError):
        to_snake_case([])

def test_to_camel_case():
    assert to_camel_case("hello_world") == "helloWorld"
    assert to_camel_case("") == ""
    assert to_camel_case("a") == "a"
    assert to_camel_case("xml_http_request") == "xmlHttpRequest"

    with pytest.raises(TypeError):
        to_camel_case(123)
    with pytest.raises(TypeError):
        to_camel_case(None)
    with pytest.raises(TypeError):
        to_camel_case([])