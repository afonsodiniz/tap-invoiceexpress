"""REST client handling, including InvoiceExpressStream base class."""

from __future__ import annotations

import sys
from typing import Any, Callable, Iterable

import requests
import logging
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator, SinglePagePaginator, BasePageNumberPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]

SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"

DEFAULT_START_DATE = '2023-01-01T10:00:00.000000Z'

class InvoiceExpressStream(RESTStream):
    """InvoiceExpress stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""

        return "https://rauvaservicesunip.app.invoicexpress.com"

    records_jsonpath = "$.invoices[*]"  # Or override `parse_response`.

    # Set this value or override `get_new_paginator`.
    next_page_token_jsonpath = "$.next_page"  # noqa: S105

    @property
    def http_headers(self) -> dict:
        """Return the HTTP headers needed.
        Returns:
            A dictionary of HTTP headers.
        """
        headers = {
            "accept": "application/json",
            "Cookie": "_makeover_app_ix_com_session=c72661d24cd0c433bb1883ec590225da"
        }

        return headers
    
    @property
    def authenticator(self) -> APIKeyAuthenticator:
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="api_key",
            value=self.config.get("api_key", ""),
            location="params",
        )


    def get_new_paginator(self) -> BaseAPIPaginator:
        """Create a new pagination helper instance.
        Returns:
            A pagination helper instance.
        """
        return BasePageNumberPaginator(start_value=1)

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization"""

        # params: dict = {
        #     "api_key": '88ed9dc4797876277ed806ef178ed073dd3a565d',
        # }
        params = {}

        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        
        start_date_val=self.config.get("start_date")
        if start_date_val:
            params["start"]  = self.config.get("start_date")
        else:
            params["start"] = DEFAULT_START_DATE
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        try:
            data = response.json()
            logger.debug(f"API response content: {data}")
        except ValueError as e:
            logger.error(f"Failed to decode JSON from response: {e}")

        logger.debug(f"API response content: {response.json()}")

        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

