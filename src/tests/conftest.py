import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

import pytest
from flask import url_for

from app import create_app, db
from config import get_logger


class MockFlaskClient:
    """Mock client implementation to make server requests."""

    _default_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self, database, config: str='default', log=None):
        self.app = create_app(config)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        database.app = self.app
        self.database = database
        self.log = log or get_logger('errors')

    def finalize(self):
        self.app_context.pop()
        self.app_context = None
        self.app = None

    def json(self,
             endpoint: str,
             headers: dict=None,
             data: dict = None,
             method: str='GET'):

        headers = headers or {}
        headers.update(self._default_headers)
        try:
            response = self.client.open(
                url_for(endpoint),
                method=method,
                data=json.dumps(data or {}),
                headers=headers)
        except Exception as e:
            self.log.error('Failed to query endpoint %s. Error:', endpoint)
            self.log.error('-' * 80)
            for line in str(e).split('\n'):
                self.log.error(line)
            self.log.error('-' * 80)
            return {}
        else:
            return json.loads(response.get_data(as_text=True))


@pytest.fixture()
def client(request):
    mock_client = MockFlaskClient(db, config='testing')
    request.addfinalizer(mock_client.finalize)
    return mock_client
