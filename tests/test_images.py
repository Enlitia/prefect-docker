from unittest.mock import AsyncMock, MagicMock

import pytest
from prefect.logging import disable_run_logger

from prefect_docker.images import pull_docker_image


class TestPullDockerImage:
    async def test_tag_and_all_tags(self, mock_docker_client_from_env: MagicMock):
        pull_kwargs = dict(repository="prefecthq/prefect", tag="latest", all_tags=True)
        with pytest.raises(
            ValueError, match="Cannot pass `tags` and `all_tags` together"
        ):
            with disable_run_logger():
                await pull_docker_image.fn(**pull_kwargs)

    async def test_defaults(self, mock_docker_client_from_env: MagicMock):
        with disable_run_logger():
            image_id = await pull_docker_image.fn(repository="prefecthq/prefect")
        assert image_id == "id_1"

    async def test_host(self, mock_docker_host: MagicMock):
        pull_kwargs = dict(
            repository="prefecthq/prefect",
        )
        with disable_run_logger():
            image_id = await pull_docker_image.fn(
                docker_host=mock_docker_host, **pull_kwargs
            )
        assert image_id == "id_1"

        client = mock_docker_host.get_client()
        client.__enter__.return_value.images.pull.assert_called_once_with(**pull_kwargs)

    async def test_login(
        self,
        mock_docker_host: MagicMock,
        mock_docker_registry_credentials: AsyncMock,
    ):
        pull_kwargs = dict(
            repository="prefecthq/prefect",
            tag="latest",
        )
        with disable_run_logger():
            image_id = await pull_docker_image.fn(
                docker_host=mock_docker_host,
                docker_registry_credentials=mock_docker_registry_credentials,
                **pull_kwargs
            )
        assert image_id == "id_1"

        client = mock_docker_host.get_client()
        client.__enter__.return_value.images.pull.assert_called_once_with(**pull_kwargs)

    async def test_all_tags(self, mock_docker_host: MagicMock):
        pull_kwargs = dict(repository="prefecthq/prefect", all_tags=True)
        with disable_run_logger():
            image_ids = await pull_docker_image.fn(
                docker_host=mock_docker_host, **pull_kwargs
            )
        assert image_ids == ["id_1", "id_2"]

        client = mock_docker_host.get_client()
        client.__enter__.return_value.images.pull.assert_called_once_with(**pull_kwargs)
