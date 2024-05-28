"""Stream type classes for tap-invoiceexpress."""

from __future__ import annotations

import sys
import typing as t

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_invoiceexpress.client import InvoiceExpressStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"


class InvoicesStream(InvoiceExpressStream):
    """Stream for Invoices endpoint"""

    name = "invoices"
    path = "/invoices.json"
    primary_keys = ["id"]

    schema_filepath = SCHEMAS_DIR / "invoices.json"  # noqa: ERA001
