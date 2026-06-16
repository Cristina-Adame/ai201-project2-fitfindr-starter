from tools import search_listings

def test_search_returns_results():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0

def test_search_empty_results():
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []

def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)
    assert all(item["price"] <= 10 for item in results)

def test_search_returns_dicts():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert all(isinstance(item, dict) for item in results)

def test_search_max_three_results():
    results = search_listings("vintage", size=None, max_price=100)
    assert len(results) <= 3

from tools import suggest_outfit
from utils.data_loader import get_example_wardrobe, get_empty_wardrobe

SAMPLE_ITEM = {
    'title': 'Graphic Tee — 2003 Tour Bootleg Style',
    'category': 'tops',
    'style_tags': ['graphic tee', 'vintage', 'grunge'],
    'colors': ['black'],
    'description': 'Vintage-style bootleg tee'
}

def test_suggest_outfit_returns_string():
    result = suggest_outfit(SAMPLE_ITEM, get_example_wardrobe())
    assert isinstance(result, str)
    assert len(result) > 0

def test_suggest_outfit_empty_wardrobe():
    result = suggest_outfit(SAMPLE_ITEM, get_empty_wardrobe())
    assert isinstance(result, str)
    assert len(result) > 0

from tools import create_fit_card

SAMPLE_OUTFIT = "Pair with baggy jeans and combat boots for a grunge look."
SAMPLE_ITEM = {
    'title': 'Graphic Tee — 2003 Tour Bootleg Style',
    'category': 'tops',
    'style_tags': ['graphic tee', 'vintage', 'grunge'],
    'colors': ['black'],
    'description': 'Vintage-style bootleg tee',
    'price': 24.0,
    'platform': 'depop'
}

def test_create_fit_card_returns_string():
    result = create_fit_card(SAMPLE_OUTFIT, SAMPLE_ITEM)
    assert isinstance(result, str)
    assert len(result) > 0

def test_create_fit_card_empty_outfit():
    result = create_fit_card("", SAMPLE_ITEM)
    assert "Error" in result