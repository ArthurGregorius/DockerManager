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
