from unittest.mock import AsyncMock, MagicMock, patch

import docker
import pytest


def mock_images_pull(all_tags=False, **kwargs):
    tags_list = [MagicMock(id="id_1"), MagicMock(id="id_2")]
    return tags_list if all_tags else tags_list[0]


@pytest.fixture
def mock_docker_client():
    client = MagicMock(_authenticated=False)
    client.return_value.__enter__.return_value.images.pull.side_effect = (
        mock_images_pull
    )
    client.__enter__.return_value.images.pull.side_effect = mock_images_pull
    return client


@pytest.fixture
def mock_docker_client_new(mock_docker_client) -> MagicMock:
    with patch.object(
        docker.DockerClient, "__new__", mock_docker_client
    ) as magic_docker_client:
        yield magic_docker_client


@pytest.fixture
def mock_docker_client_from_env(mock_docker_client) -> MagicMock:
    with patch.object(
        docker.DockerClient, "from_env", mock_docker_client
    ) as magic_docker_client:
        yield magic_docker_client


@pytest.fixture
def mock_docker_host(mock_docker_client):
    docker_host = MagicMock()
    docker_host.get_client.side_effect = lambda: mock_docker_client
    return docker_host


@pytest.fixture
def mock_docker_registry_credentials():
    docker_registry_credentials = AsyncMock()
    docker_registry_credentials.login.side_effect = lambda client: setattr(
        client, "_authenticated", True
    )
    return docker_registry_credentials
