import json, os
import card_data as D

def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

def run(R, A):
    Dd = f"{R}/data/tarot"
    item_ids = [f"card_{c[0]}" for c in D.CARDS] + list(D.ITEMS.keys())
    for n in item_ids:
        dump(f"{A}/items/{n}.json", {"model": {"type": "minecraft:model", "model": f"tarot:item/{n}"}})
        dump(f"{A}/models/item/{n}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"tarot:item/{n}"}})
    dump(f"{A}/models/block/tarot_table.json", {"parent": "minecraft:block/cube_bottom_top", "textures": {"top": "tarot:block/tarot_table_top", "side": "tarot:block/tarot_table_side", "bottom": "tarot:block/tarot_table_bottom"}})
    dump(f"{A}/models/block/arcane_altar.json", {"parent": "minecraft:block/cube_bottom_top", "textures": {"top": "tarot:block/arcane_altar_top", "side": "tarot:block/arcane_altar_side", "bottom": "tarot:block/arcane_altar_side"}})
    for b in ("tarot_table", "arcane_altar"):
        dump(f"{A}/blockstates/{b}.json", {"variants": {"": {"model": f"tarot:block/{b}"}}})
        dump(f"{A}/items/{b}.json", {"model": {"type": "minecraft:model", "model": f"tarot:block/{b}"}})
        dump(f"{Dd}/loot_table/blocks/{b}.json", {"type": "minecraft:block", "random_sequence": f"tarot:blocks/{b}", "pools": [{"rolls": 1, "bonus_rolls": 0, "entries": [{"type": "minecraft:item", "name": f"tarot:{b}"}], "conditions": [{"condition": "minecraft:survives_explosion"}]}]})
    dump(f"{R}/data/minecraft/tags/block/mineable/axe.json", {"replace": False, "values": ["tarot:tarot_table"]})
    dump(f"{R}/data/minecraft/tags/block/mineable/pickaxe.json", {"replace": False, "values": ["tarot:arcane_altar"]})

    # ---- recetas (el sobre YA NO se craftea: se obtiene en Santuarios, con El Vidente o con profecías)
    old = f"{Dd}/recipe/booster_pack.json"
    if os.path.exists(old): os.remove(old)
    dump(f"{Dd}/recipe/stardust.json", {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": ["minecraft:amethyst_shard", "minecraft:glowstone_dust"], "result": {"id": "tarot:stardust", "count": 2}})
    dump(f"{Dd}/recipe/tarot_table.json", {"type": "minecraft:crafting_shaped", "category": "misc", "pattern": ["AGA", "OBO", "OOO"], "key": {"A": "minecraft:amethyst_shard", "G": "minecraft:gold_ingot", "O": "minecraft:obsidian", "B": "minecraft:book"}, "result": {"id": "tarot:tarot_table", "count": 1}})
    dump(f"{Dd}/recipe/grimoire.json", {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": ["minecraft:book", "minecraft:amethyst_shard"], "result": {"id": "tarot:grimoire", "count": 1}})
    dump(f"{Dd}/recipe/destiny_deck.json", {"type": "minecraft:crafting_shaped", "category": "misc", "pattern": ["PPP", "PSP", "PPP"], "key": {"P": "minecraft:paper", "S": "tarot:stardust"}, "result": {"id": "tarot:destiny_deck", "count": 1}})
    dump(f"{Dd}/recipe/arcane_altar.json", {"type": "minecraft:crafting_shaped", "category": "misc", "pattern": ["ODO", "STS", "OOO"], "key": {"O": "minecraft:obsidian", "D": "minecraft:diamond", "S": "tarot:stardust", "T": "tarot:tarot_table"}, "result": {"id": "tarot:arcane_altar", "count": 1}})

    # ---- logros (se otorgan por código con criterio "impossible")
    adv = [("first_card", None, "card_fool", "task", "background"),
           ("apprentice", "first_card", "card_priestess", "task", None),
           ("defy_fate", "apprentice", "tarot_table", "goal", None),
           ("arcana_hunter", "defy_fate", "destiny_heart", "goal", None),
           ("cosmos_lord", "arcana_hunter", "card_world", "challenge", None)]
    for aid, parent, icon, frame, bg in adv:
        d = {"display": {"icon": {"id": f"tarot:{icon}"}, "title": {"translate": f"advancements.tarot.{aid}.title"},
                         "description": {"translate": f"advancements.tarot.{aid}.desc"}, "frame": frame, "show_toast": True,
                         "announce_to_chat": frame != "task", "hidden": False},
             "criteria": {"done": {"trigger": "minecraft:impossible"}}}
        if parent: d["parent"] = f"tarot:{parent}"
        if bg: d["display"]["background"] = "minecraft:gui/advancements/backgrounds/adventure"
        dump(f"{Dd}/advancement/{aid}.json", d)

    ADV = {"first_card": ("Primera Carta", "Obtené tu primera carta del Tarot.", "First Card", "Obtain your first Tarot card."),
           "apprentice": ("Aprendiz de Vidente", "Registrá 5 cartas distintas en tu colección.", "Seer's Apprentice", "Register 5 different cards."),
           "defy_fate": ("Desafiar al Destino", "Completá tu primera profecía en la Mesa del Tarot.", "Defy Fate", "Fulfil your first prophecy."),
           "arcana_hunter": ("Cazador de Arcanos", "Derrotá a un jefe invocado en el Altar Arcano.", "Arcana Hunter", "Defeat a boss summoned at the Arcane Altar."),
           "cosmos_lord": ("Señor del Cosmos", "Forjá una carta Cósmica.", "Lord of the Cosmos", "Forge a Cosmic card.")}
    for idx, es in enumerate((True, False)):
        pass
    for f, es in {"en_us": False, "es_es": True, "es_mx": True, "es_ar": True, "es_uy": True}.items():
        L = {"itemGroup.tarot": "Arcanos: Tarot" if es else "Arcana: Tarot",
             "block.tarot.tarot_table": "Mesa del Tarot" if es else "Tarot Table",
             "block.tarot.arcane_altar": "Altar Arcano" if es else "Arcane Altar",
             "container.tarot.tarot_table": "Mesa del Tarot" if es else "Tarot Table",
             "key.tarot.open_tree": "Abrir Árbol del Destino" if es else "Open Destiny Tree",
             "key.category.tarot.main": "Arcanos: Tarot" if es else "Arcana: Tarot",
             "key.tarot.debug_menu": "Menú de prueba (creativo)" if es else "Test menu (creative)",
             "entity.tarot.hierophant": "El Hierofante Corrompido" if es else "The Corrupted Hierophant",
             "entity.tarot.moon_shadow": "La Sombra de la Luna" if es else "Shadow of the Moon",
             "entity.tarot.last_judgement": "El Juicio Final" if es else "The Last Judgement"}
        for k, (e, n) in D.ITEMS.items(): L[f"item.tarot.{k}"] = e if es else n
        for c in D.CARDS:
            cid = c[0]
            L[f"item.tarot.card_{cid}"] = c[2] if es else c[3]
            L[f"tooltip.tarot.{cid}.active"] = c[4] if es else c[5]
            L[f"tooltip.tarot.{cid}.passive"] = c[6] if es else c[7]
        for aid, t in ADV.items():
            L[f"advancements.tarot.{aid}.title"] = t[0] if es else t[2]
            L[f"advancements.tarot.{aid}.desc"] = t[1] if es else t[3]
        dump(f"{A}/lang/{f}.json", L)
