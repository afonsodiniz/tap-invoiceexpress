"""InvoiceExpress tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_invoiceexpress import streams


class TapInvoiceExpress(Tap):
    """InvoiceExpress tap class."""

    name = "tap-invoiceexpress"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True,
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        # th.Property(
        #     "account_type",
        #     th.StringType,
        #     required=True,
        #     description="Type of the account ('tech' or 'services') to specify which API URL to use",
        # )
    ).to_dict()

    def discover_streams(self) -> list[streams.InvoiceExpressStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.InvoicesStream(self)
        ]


if __name__ == "__main__":
    TapInvoiceExpress.cli()
