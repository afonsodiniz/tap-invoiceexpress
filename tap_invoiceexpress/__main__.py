"""InvoiceExpress entry point."""

from __future__ import annotations

from tap_invoiceexpress.tap import TapInvoiceExpress

TapInvoiceExpress.cli()
