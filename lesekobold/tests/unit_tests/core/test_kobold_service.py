import uuid

import pytest
from src.core.kobold_service import KoboldService


@pytest.fixture
def kobold_service() -> KoboldService:
    return KoboldService(name="test_kobold_service")


@pytest.mark.unit_test
def test_kobold_service_init(kobold_service: KoboldService):
    assert kobold_service is not None
    assert kobold_service.name == "test_kobold_service"
    assert kobold_service.session_manager is not None
    assert kobold_service.agent is not None
    assert kobold_service.runner is not None


@pytest.mark.unit_test
@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.makes_api_call
async def test_kobold_service_run(kobold_service: KoboldService):
    user_id = uuid.uuid4()
    session_id = None
    final_msg, response_attachments = await kobold_service.run(
        prompt="Write a story about a cat for grade 2.",
        user_id=user_id,
        session_id=session_id,
    )
    assert final_msg is not None
    assert response_attachments is not None
    assert len(response_attachments) > 0
    assert response_attachments is not None
    assert len(response_attachments) > 0
