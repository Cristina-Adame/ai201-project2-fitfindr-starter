from tools import suggest_outfit
from utils.data_loader import get_example_wardrobe, get_empty_wardrobe

item = {
    'title': 'Graphic Tee — 2003 Tour Bootleg Style',
    'category': 'tops',
    'style_tags': ['graphic tee', 'vintage', 'grunge'],
    'colors': ['black'],
    'description': 'Vintage-style bootleg tee'
}

# Test with example wardrobe
print("=== With wardrobe ===")
print(suggest_outfit(item, get_example_wardrobe()))

print("\n=== Empty wardrobe ===")
print(suggest_outfit(item, get_empty_wardrobe()))