from tools import search_listings, suggest_outfit, create_fit_card
from utils.data_loader import get_example_wardrobe

results = search_listings("vintage graphic tee", size=None, max_price=30)
item = results[0]
outfit = suggest_outfit(item, get_example_wardrobe())
print("=== Fit Card ===")
print(create_fit_card(outfit, item))

print("\n=== Empty outfit test ===")
print(create_fit_card("", item))