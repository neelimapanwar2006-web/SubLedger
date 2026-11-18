def base(c,active=True,price="100"):
    p=c.post("/api/plans",json={"name":"Basic","price":price,"is_active":active})
    u=c.post("/api/customers",json={"name":"Asha","email":"asha@example.com"})
    return p.json(),u.json()
def sub(c,p,u): return c.post("/api/subscriptions",json={"plan_id":p["id"],"customer_id":u["id"]})
def test_plan_price_positive(client):
    assert client.post("/api/plans",json={"name":"Zero","price":"0"}).status_code==422
def test_unique_customer_email(client):
    d={"name":"Asha","email":"asha@example.com"}
    assert client.post("/api/customers",json=d).status_code==201
    assert client.post("/api/customers",json=d).status_code==409
def test_inactive_plan_rejected(client):
    p,u=base(client,active=False)
    assert sub(client,p,u).status_code==400
def test_duplicate_active_subscription_rejected(client):
    p,u=base(client)
    assert sub(client,p,u).status_code==201
    assert sub(client,p,u).status_code==409
def test_invoice_snapshots_plan_price_and_ledger(client):
    p,u=base(client,price="125")
    s=sub(client,p,u).json()
    inv=client.post("/api/invoices",json={"subscription_id":s["id"]})
    assert inv.status_code==201 and inv.json()["amount_due"]=="125.00"
    assert client.get("/api/ledger").json()[0]["event_type"]=="invoice_created"
def test_partial_then_full_payment(client):
    p,u=base(client); s=sub(client,p,u).json()
    i=client.post("/api/invoices",json={"subscription_id":s["id"]}).json()
    url=f"/api/invoices/{i['id']}/payments"
    a=client.post(url,json={"amount":"40","status":"succeeded","provider_reference":"ref-1"})
    assert a.json()["invoice"]["status"]=="partially_paid"
    b=client.post(url,json={"amount":"60","status":"succeeded","provider_reference":"ref-2"})
    assert b.json()["invoice"]["status"]=="paid"
def test_failed_payment_and_overpayment(client):
    p,u=base(client); s=sub(client,p,u).json()
    i=client.post("/api/invoices",json={"subscription_id":s["id"]}).json(); url=f"/api/invoices/{i['id']}/payments"
    f=client.post(url,json={"amount":"25","status":"failed","provider_reference":"fail-1"})
    assert f.json()["invoice"]["amount_paid"]=="0.00"
    assert client.post(url,json={"amount":"101","status":"succeeded","provider_reference":"over-1"}).status_code==400

def test_deactivate_plan(client):
    p, u = base(client)

    response = client.patch(
        f"/api/plans/{p['id']}",
        json={"is_active": False}
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_reactivate_plan(client):
    p, u = base(client, active=False)

    response = client.patch(
        f"/api/plans/{p['id']}",
        json={"is_active": True}
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is True

    # An active plan should now allow a subscription.
    assert sub(client, p, u).status_code == 201


def test_update_nonexistent_plan(client):
    response = client.patch(
        "/api/plans/9999",
        json={"is_active": False}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Plan not found"
