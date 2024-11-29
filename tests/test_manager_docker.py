# tests/test_manager_docker.py
import pytest
import docker
from src.manager_docker import get_docker_version, create_container

@pytest.fixture(scope="module")
def docker_client():
    # Setup Docker client
    client = docker.from_env()
    yield client
    # Teardown: Optional, jika Anda ingin membersihkan container atau resources
    client.close()

def test_get_docker_version(docker_client):
    # Uji apakah get_docker_version menghasilkan output yang valid
    version = get_docker_version()
    assert "ApiVersion" in version
    assert "Version" in version

def test_create_container(docker_client):
    # Uji apakah create_container membuat container yang benar
    image_name = "alpine"
    container_id = create_container(image_name)
    assert container_id is not None
    assert len(container_id) > 0

    # Cleanup: Hapus container yang telah dibuat
    container = docker_client.containers.get(container_id)
    container.stop()
    container.remove()
