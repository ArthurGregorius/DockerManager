import pytest
from unittest import mock
from docker.errors import NotFound, APIError
from manager_docker import (
    list_containers,
    start_container,
    stop_container,
    remove_container,
    create_container,
)

# Mocking Docker client
@pytest.fixture
def mock_docker_client():
    # Membuat objek mock untuk docker.client
    mock_client = mock.Mock()
    return mock_client

# 1. Test untuk list_containers
def test_list_containers(mock_docker_client):
    # Menyiapkan mock behavior
    mock_container = mock.Mock()
    mock_container.name = "container_1"
    mock_container.id = "12345"
    mock_container.status = "running"
    mock_docker_client.containers.list.return_value = [mock_container]

    with mock.patch('docker.from_env', return_value=mock_docker_client):
        # Panggil fungsi list_containers
        with mock.patch('builtins.print') as mock_print:
            list_containers()

            # Verifikasi bahwa output print adalah seperti yang diharapkan
            mock_print.assert_any_call("\nDaftar Container yang Aktif:\n")
            mock_print.assert_any_call(f"ID: {mock_container.id}, Nama: {mock_container.name}, Status: {mock_container.status}")

# 2. Test untuk start_container
def test_start_container(mock_docker_client):
    # Menyiapkan mock behavior
    mock_container = mock.Mock()
    mock_container.start.return_value = None
    mock_docker_client.containers.get.return_value = mock_container

    with mock.patch('docker.from_env', return_value=mock_docker_client):
        with mock.patch('builtins.print') as mock_print:
            start_container("container_1")

            # Verifikasi bahwa container start dipanggil
            mock_container.start.assert_called_once()
            mock_print.assert_any_call("Container container_1 telah dimulai.")

# 3. Test untuk stop_container
def test_stop_container(mock_docker_client):
    # Menyiapkan mock behavior
    mock_container = mock.Mock()
    mock_container.stop.return_value = None
    mock_docker_client.containers.get.return_value = mock_container

    with mock.patch('docker.from_env', return_value=mock_docker_client):
        with mock.patch('builtins.print') as mock_print:
            stop_container("container_1")

            # Verifikasi bahwa container stop dipanggil
            mock_container.stop.assert_called_once()
            mock_print.assert_any_call("Container container_1 telah dihentikan.")

# 4. Test untuk remove_container
def test_remove_container(mock_docker_client):
    # Menyiapkan mock behavior
    mock_container = mock.Mock()
    mock_container.remove.return_value = None
    mock_docker_client.containers.get.return_value = mock_container

    with mock.patch('docker.from_env', return_value=mock_docker_client):
        with mock.patch('builtins.print') as mock_print:
            remove_container("container_1")

            # Verifikasi bahwa container remove dipanggil
            mock_container.remove.assert_called_once_with(force=True)
            mock_print.assert_any_call("Container container_1 telah dihapus.")

# 5. Test untuk create_container
def test_create_container(mock_docker_client):
    # Menyiapkan mock behavior
    mock_container = mock.Mock()
    mock_container.name = "container_1"
    mock_docker_client.containers.run.return_value = mock_container

    with mock.patch('docker.from_env', return_value=mock_docker_client):
        with mock.patch('builtins.print') as mock_print:
            create_container("python:3.9", "container_1", ports={"5000": "5000"})

            # Verifikasi bahwa container run dipanggil
            mock_docker_client.containers.run.assert_called_once_with(
                "python:3.9", detach=True, name="container_1", ports={"5000": "5000"}, volumes=None
            )
            mock_print.assert_any_call(f"Container baru telah dibuat: {mock_container.name}")

# 6. Test untuk error handling (contoh untuk NotFound exception)
def test_start_container_notfound(mock_docker_client):
    mock_docker_client.containers.get.side_effect = NotFound("Container tidak ditemukan")

    with mock.patch('docker.from_env', return_value=mock_docker_client):
        with mock.patch('builtins.print') as mock_print:
            start_container("container_1")

            # Verifikasi bahwa error message dicetak
            mock_print.assert_any_call("Container container_1 tidak ditemukan.")

# 7. Test untuk error handling (contoh untuk APIError exception)
def test_create_container_apierror(mock_docker_client):
    mock_docker_client.containers.run.side_effect = APIError("Docker API Error", None)

    with mock.patch('docker.from_env', return_value=mock_docker_client):
        with mock.patch('builtins.print') as mock_print:
            create_container("python:3.9", "container_1", ports={"5000": "5000"})

            # Verifikasi bahwa error message dicetak
            mock_print.assert_any_call("Terjadi kesalahan saat membuat container: Docker API Error")
