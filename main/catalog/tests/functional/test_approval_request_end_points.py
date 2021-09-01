""" Test order end points """
import json
import pytest
from django.urls import reverse

from main.catalog.tests.factories import ApprovalRequestFactory


@pytest.mark.django_db
def test_order_approval_request_get(api_request):
    """Get List of approval requests of an order item"""
    approval_request = ApprovalRequestFactory()

    response = api_request(
        "get",
        reverse(
            "order-approvalrequest-list",
            args=(approval_request.order.id,),
        ),
    )

    assert response.status_code == 200

    data = response.data
    assert data["id"] == approval_request.id
    assert (
        data["approval_request_ref"] == approval_request.approval_request_ref
    )
    assert data["reason"] == approval_request.reason