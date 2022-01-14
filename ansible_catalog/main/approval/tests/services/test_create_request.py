""" Module to test creating requests """
from unittest.mock import Mock
import pytest
from ansible_catalog.main.tests.factories import default_tenant
from ansible_catalog.main.approval.tests.factories import WorkflowFactory
from ansible_catalog.main.approval.services.create_request import CreateRequest
from ansible_catalog.main.approval.services.link_workflow import FindWorkflows
from ansible_catalog.main.approval.tasks import process_root_task


@pytest.mark.django_db
def test_create_request_no_workflow(mocker):
    """Test to create a new request with no workflow"""

    enqueue = mocker.patch("django_rq.enqueue", return_value=Mock(id=123))
    service = _prepare_service()
    request = service.process().request
    _assert_request(request)
    enqueue.assert_called_once_with(process_root_task, request.id, [])


@pytest.mark.django_db
def test_create_request_with_workflow(mocker):
    """Test to create a new request with one workflow but no group"""

    enqueue = mocker.patch("django_rq.enqueue", return_value=Mock(id=123))
    workflow = WorkflowFactory()
    mocker.patch.object(
        FindWorkflows, "process", return_value=Mock(workflows=(workflow,))
    )
    service = _prepare_service()
    request = service.process().request
    _assert_request(request)
    enqueue.assert_called_once_with(
        process_root_task, request.id, [workflow.id]
    )


def _prepare_service():
    tenant = default_tenant()
    service = CreateRequest(
        {
            "name": "test",
            "description": "description",
            "content": {"param": "val"},
            "tenant": tenant,
        }
    )
    return service


def _assert_request(request, num_children=0, group_name="", workflow=None):
    assert request.name == "test"
    assert request.description == "description"
    assert request.state == "pending"
    assert request.decision == "undecided"
    assert request.number_of_children == num_children
    assert request.workflow == workflow
    assert request.group_name == group_name
