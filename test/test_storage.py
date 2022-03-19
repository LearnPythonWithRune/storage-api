from unittest.mock import mock_open, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize('test_file', ['file_foo', 'file_bar'])
@pytest.mark.parametrize('test_data', ['banana', 'apple', 'pear'])
def test_post_create_file(test_file, test_data):
    # https://docs.python.org/3.3/library/unittest.mock.html#mock-open
    m = mock_open()
    with patch('app.routes.storage.open', m, create=True):
        response = client.post(
            '/create_file',
            params={'filename': test_file,
                    'file_data': test_data}
        )
    assert response.status_code == 200
    assert response.json() == {'Create': 'OK'}
    assert m.call_count == 1
    m.assert_called_once_with(f'my_storage/{test_file}', 'w')
    handle = m()
    handle.write.assert_called_once_with(test_data)
