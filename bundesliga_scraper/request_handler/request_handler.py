"""Handles all requests by the user."""

from __future__ import annotations

from bundesliga_scraper.request_handler.fixture_request_handler import (
    handle_fixture_request,
)
from bundesliga_scraper.request_handler.table_request_handler import (
    handle_table_request,
)


def handle_args(user_args: dict[str, str | int]) -> None:
    """Handling the arguments given by the user.

    Args:
        user_args (dict[str, str | int]): dict of key value pairs given by the user
    """
    if not user_args["table"] and not user_args["fixture"]:
        return

    if user_args["table"]:
        handle_table_request(user_args)

    if user_args["fixture"]:
        handle_fixture_request(user_args)
