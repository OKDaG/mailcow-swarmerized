import unittest
import json
import docker

from unittest.mock import patch, MagicMock

from dockerapi import nodes_containers_get, is_swarm_mode


def mock_dockerapi_tasks():
    return ['10.10.10.1', '10.10.10.2']

def mocked_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, status, result):
            self.status = status
            self.result = result

        def json(self):
            return self.result

    return MockResponse(200, None)

@patch('dockerapi.get_dockerapi_tasks', side_effect=mock_dockerapi_tasks)
@patch('requests.get', side_effect=mocked_requests)
class TestNodeContainers(unittest.TestCase):

    @patch('dockerapi.docker_client')
    def test_swarm_mode_if_swarm_update_cannot_be_processed(self, docker_client_mock, dockerapi_nodes_mock, request_mock):
        docker_client_mock.swarm.update.side_effect = AttributeError("something  wrong")
        self.assertFalse(is_swarm_mode())

    @patch('dockerapi.docker_client')
    def test_swarm_mode_if_swarm_update_raise_api_error(self, docker_client_mock, dockerapi_nodes_mock, request_mock):
        docker_client_mock.swarm.update.side_effect = docker.errors.APIError("something wrong")

        self.assertFalse(is_swarm_mode())

    @patch('dockerapi.docker_client')
    def test_swarm_mode_if_swarm_in_swarm(self, dockerapi_nodes_mock, request_mock, docker_client_mock):
        docker_client_mock.swarm = MagicMock()

        self.assertTrue(is_swarm_mode())

    def test_nothing(self, dockerapi_nodes_mock, request_mock):
        nodes_container = nodes_containers_get().get()

        self.assertNotEqual(nodes_container, None)


if __name__ == '__main__':
    unittest.main()
