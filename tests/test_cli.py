import pytest

from cli import get_xml_encoding


@pytest.mark.parametrize('value, result', [
    [b'<?xml version="1.0" encoding="windows-1251"?>\r\n', 'windows-1251'],
    [b'<?xml version="1.0" encoding="utf-8"?>\r\n', 'utf-8'],
    [b"<?xml version='1.0' encoding='utf-8'?>\r\n", 'utf-8'],
    [b'<?xml version="1.0"?>\r\n', None],
])
def test_get_xml_encoding(value, result):
    assert get_xml_encoding(value) == result
