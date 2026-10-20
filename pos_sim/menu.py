"""
Built-in default restaurant (used when llm=False, and as the fallback when the LLM's output fails
validation). Same schema the LLM must return.
"""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal

Category = Literal["Appetizers", "Entrees", "Sandwiches", "Salads", "Sides", "Desserts", "Beer", "Wine", "Cocktails", "Non-Alcoholic", "Brunch", "Late Night"]
PRICE_RANGE = {"Appetizers": (6, 18), "Entrees": (12, 38), "Sandwiches": (10, 20), "Salads": (9, 18), "Sides": (3, 9),
               "Desserts": (6, 12), "Beer": (3, 9), "Wine": (7, 16), "Cocktails": (8, 15), "Non-Alcoholic": (2, 6),
               "Brunch": (9, 18), "Late Night": (6, 15)}
ALCOHOL = {"Beer", "Wine", "Cocktails"}


class Modifier(BaseModel):
    name: str = Field(max_length=40)
    price: float = Field(ge=0, le=4)


class MenuItem(BaseModel):
    name: str = Field(max_length=40)
    category: Category
    price: float = Field(gt=0, le=60)
    modifiers: list[Modifier] = Field(default_factory=list, max_length=3)
    popularity: float = Field(1.0, gt=0, le=5, description="relative weight within its category")


class Restaurant(BaseModel):
    name: str = Field(max_length=40)
    concept: str = Field(max_length=80)
    servers: list[str] = Field(min_length=3, max_length=12)
    items: list[MenuItem] = Field(min_length=15, max_length=60)

    def check(self) -> list[str]:
        """Guardrail check beyond the schema: price ranges per category, category coverage."""
        problems = []
        for it in self.items:
            lo, hi = PRICE_RANGE[it.category]
            if not (lo <= it.price <= hi):
                problems.append(f"{it.name}: ${it.price} outside {it.category} range {lo}-{hi}")
        cats = {it.category for it in self.items}
        for need in ("Appetizers", "Entrees", "Non-Alcoholic"):
            if need not in cats:
                problems.append(f"missing category {need}")
        return problems


def M(name, cat, price, pop=1.0, mods=()):
    return MenuItem(name=name, category=cat, price=price, popularity=pop, modifiers=[Modifier(name=n, price=p) for n, p in mods])


DEFAULT = Restaurant(
    name="Market Street Grill", concept="downtown full-service American grill with a bar",
    servers=["Alex", "Jordan", "Sam", "Casey", "Riley", "Morgan", "Devin", "Taylor"],
    items=[
        M("Fried Pickles", "Appetizers", 9, 1.4, [("Extra ranch", 0.75)]),
        M("Wings (10)", "Appetizers", 14, 1.8, [("Hot", 0), ("Garlic parm", 0), ("Extra sauce", 0.5)]),
        M("Pimento Cheese Dip", "Appetizers", 10, 0.9),
        M("Loaded Fries", "Appetizers", 11, 1.1),
        M("Grill Burger", "Sandwiches", 15, 2.2, [("Add bacon", 2), ("No onion", 0), ("Sub salad", 1.5)]),
        M("Fried Chicken Sandwich", "Sandwiches", 14, 1.6, [("Spicy", 0)]),
        M("Smoked Turkey Club", "Sandwiches", 13, 0.8),
        M("Ribeye (12 oz)", "Entrees", 34, 0.9, [("Add shrimp", 4)]),
        M("Grilled Salmon", "Entrees", 26, 1.0),
        M("Shrimp & Grits", "Entrees", 22, 1.2),
        M("Pan Roasted Chicken", "Entrees", 21, 1.1, [("Sub veg", 0)]),
        M("Meatloaf Plate", "Entrees", 18, 0.9),
        M("Market Salad", "Salads", 12, 0.9, [("Add chicken", 4), ("Add salmon", 4)]),
        M("Caesar", "Salads", 11, 0.8, [("Add chicken", 4)]),
        M("Fries", "Sides", 5, 1.5), M("Mac & Cheese", "Sides", 6, 1.0), M("Collards", "Sides", 5, 0.5),
        M("Chocolate Cake", "Desserts", 9, 0.7), M("Bread Pudding", "Desserts", 8, 0.6),
        M("Draft IPA", "Beer", 7, 2.0), M("Draft Lager", "Beer", 6, 1.8), M("Can Domestic", "Beer", 4, 1.2),
        M("House Red", "Wine", 10, 1.0), M("House White", "Wine", 10, 1.0),
        M("Old Fashioned", "Cocktails", 12, 1.1), M("Margarita", "Cocktails", 11, 1.3), M("Espresso Martini", "Cocktails", 13, 0.7),
        M("Soda", "Non-Alcoholic", 3, 2.0, [("Refill", 0)]), M("Sweet Tea", "Non-Alcoholic", 3, 2.0), M("Coffee", "Non-Alcoholic", 3, 0.6),
        M("Late Night Burger", "Late Night", 12, 1.5), M("Late Night Wings (6)", "Late Night", 9, 1.5), M("Basket of Fries", "Late Night", 6, 1.2),
        M("Biscuits & Gravy", "Brunch", 11, 1.3), M("Chicken & Waffles", "Brunch", 15, 1.5), M("Mimosa", "Brunch", 9, 1.6),
    ],
)
