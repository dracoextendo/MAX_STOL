from fastapi import status


def test_get_index_html(test_client):
    response = test_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'] == 'text/html; charset=utf-8'