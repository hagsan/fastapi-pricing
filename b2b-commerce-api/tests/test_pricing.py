def test_get_pricing(client):
    response = client.post("/pricing", json={"products": [{"product_id": 1}, {"product_id": 2}]})
    assert response.status_code == 200
    assert "prices" in response.json()

def test_get_pricing_empty_list(client):
    response = client.post("/pricing", json={"products": []})
    assert response.status_code == 400
    assert response.json() == {"detail": "Product list cannot be empty."}

def test_get_pricing_invalid_product(client):
    response = client.post("/pricing", json={"products": [{"product_id": "invalid"}]})
    assert response.status_code == 422  # Unprocessable Entity for invalid input

def test_get_pricing_nonexistent_product(client):
    response = client.post("/pricing", json={"products": [{"product_id": 999}]})
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found."}