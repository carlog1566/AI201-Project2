# tests/test_tools.py

from tools import (
    search_listings,
    suggest_outfit,
    create_fit_card,
)
from utils.data_loader import (
    get_example_wardrobe,
    get_empty_wardrobe,
)


# ── search_listings tests ───────────────────────────────────────────

def test_search_returns_results():
    results = search_listings(
        "vintage graphic tee",
        size=None,
        max_price=50,
    )

    assert isinstance(results, list)
    assert len(results) > 0


def test_search_empty_results():
    results = search_listings(
        "designer ballgown",
        size="XXS",
        max_price=5,
    )

    assert results == []


def test_search_price_filter():
    results = search_listings(
        "jacket",
        size=None,
        max_price=10,
    )

    assert all(item["price"] <= 10 for item in results)


# ── suggest_outfit tests ────────────────────────────────────────────

def test_suggest_outfit_empty_wardrobe():
    results = search_listings(
        "vintage graphic tee",
        size=None,
        max_price=50,
    )

    outfit = suggest_outfit(
        results[0],
        get_empty_wardrobe(),
    )

    assert isinstance(outfit, str)
    assert outfit.strip() != ""


def test_suggest_outfit_example_wardrobe():
    results = search_listings(
        "vintage graphic tee",
        size=None,
        max_price=50,
    )

    outfit = suggest_outfit(
        results[0],
        get_example_wardrobe(),
    )

    assert isinstance(outfit, str)
    assert outfit.strip() != ""


# ── create_fit_card tests ───────────────────────────────────────────

def test_create_fit_card_missing_outfit():
    results = search_listings(
        "vintage graphic tee",
        size=None,
        max_price=50,
    )

    caption = create_fit_card(
        "",
        results[0],
    )

    assert isinstance(caption, str)
    assert caption.strip() != ""


def test_create_fit_card_valid_input():
    results = search_listings(
        "vintage graphic tee",
        size=None,
        max_price=50,
    )

    caption = create_fit_card(
        "Pair it with baggy jeans and chunky sneakers.",
        results[0],
    )

    assert isinstance(caption, str)
    assert caption.strip() != ""