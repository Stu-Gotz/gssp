-- This is just for posterity and I guess if people want to setup their own thing.

-- Run data_collection.py to get last 3 months of data

-- compare stats, run in backend because it makes more sense to do so
CREATE OR REPLACE FUNCTION compare_ranks(p_tier TEXT)
RETURNS TABLE (
  pokemon       TEXT,
  current_rank  INTEGER,
  previous_rank INTEGER,
  older_rank    INTEGER
)
LANGUAGE sql
STABLE
AS $$
  WITH names AS (
    SELECT c.pokemon FROM current c WHERE c.tier = p_tier AND c.rank <= 25
    UNION
    SELECT p.pokemon FROM previous p WHERE p.tier = p_tier AND p.rank <= 25
  )
  SELECT n.pokemon, c.rank, p.rank, o.rank
  FROM names n
  LEFT JOIN current  c ON c.pokemon = n.pokemon AND c.tier = p_tier
  LEFT JOIN previous p ON p.pokemon = n.pokemon AND p.tier = p_tier
  LEFT JOIN tma      o ON o.pokemon = n.pokemon AND o.tier = p_tier
  ORDER BY c.rank NULLS LAST, p.rank;
$$;

-- SAMPLE USERS and SAMPLE TEAMS
BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Makes the script safe to re-run (teams are removed by ON DELETE CASCADE)
DELETE FROM users WHERE username IN ('ash_k', 'misty_w', 'brock_h');

INSERT INTO users (username, password, email, role, profile) VALUES
  ('ash_k',   crypt('password123', gen_salt('bf', 10)), 'ash@example.com',   'user',
   '{"firstname": "Ash", "lastname": "Ketchum", "location": "Pallet Town"}'),
  ('misty_w', crypt('password123', gen_salt('bf', 10)), 'misty@example.com', 'user',
   '{"firstname": "Misty", "lastname": "Waterflower", "location": "Cerulean City"}'),
  ('brock_h', crypt('password123', gen_salt('bf', 10)), 'brock@example.com', 'admin',
   '{"firstname": "Brock", "lastname": "Harrison", "location": "Pewter City"}');

-- Ash: Gen 9 OU
INSERT INTO teams (user_id, tier, data)
SELECT id, 'gen9ou', $${
  "id": "k3j9x2abq1",
  "name": "=== gen9ou Paradox Pressure ===",
  "gen": "gen9", "tier": "ou",
  "members": [
    {"name": "great tusk", "item": "booster energy", "ability": "protosynthesis", "nature": "jolly",
     "evs": {"atk": 252, "spd": 4, "spe": 252},
     "moves": [
       {"headlong-rush": {"name": "headlong-rush", "type": "ground",   "priority": 0, "power": 120, "genre": "physical"}},
       {"close-combat":  {"name": "close-combat",  "type": "fighting", "priority": 0, "power": 120, "genre": "physical"}},
       {"rapid-spin":    {"name": "rapid-spin",    "type": "normal",   "priority": 0, "power": 50,  "genre": "physical"}},
       {"ice-spinner":   {"name": "ice-spinner",   "type": "ice",      "priority": 0, "power": 80,  "genre": "physical"}}
     ],
     "type": ["ground", "fighting"], "dex": 984,
     "spriteUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/984.png",
     "itemUrl": null},
    {"name": "gholdengo", "item": "choice scarf", "ability": "good as gold", "nature": "timid",
     "evs": {"spa": 252, "spd": 4, "spe": 252},
     "moves": [
       {"make-it-rain": {"name": "make-it-rain", "type": "steel",   "priority": 0, "power": 120,  "genre": "special"}},
       {"shadow-ball":  {"name": "shadow-ball",  "type": "ghost",   "priority": 0, "power": 80,   "genre": "special"}},
       {"trick":        {"name": "trick",        "type": "psychic", "priority": 0, "power": null, "genre": "status"}},
       {"nasty-plot":   {"name": "nasty-plot",   "type": "dark",    "priority": 0, "power": null, "genre": "status"}}
     ],
     "type": ["steel", "ghost"], "dex": 1000,
     "spriteUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1000.png",
     "itemUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/choice-scarf.png"},
    {"name": "kingambit", "item": "leftovers", "ability": "supreme overlord", "nature": "adamant",
     "evs": {"hp": 252, "atk": 252, "spd": 4},
     "moves": [
       {"swords-dance":  {"name": "swords-dance",  "type": "normal", "priority": 0, "power": null, "genre": "status"}},
       {"kowtow-cleave": {"name": "kowtow-cleave", "type": "dark",   "priority": 0, "power": 85,   "genre": "physical"}},
       {"sucker-punch":  {"name": "sucker-punch",  "type": "dark",   "priority": 1, "power": 70,   "genre": "physical"}},
       {"iron-head":     {"name": "iron-head",     "type": "steel",  "priority": 0, "power": 80,   "genre": "physical"}}
     ],
     "type": ["dark", "steel"], "dex": 983,
     "spriteUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/983.png",
     "itemUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/leftovers.png"}
  ]
}$$::jsonb
FROM users WHERE username = 'ash_k';

-- Misty: Gen 8 OU
INSERT INTO teams (user_id, tier, data)
SELECT id, 'gen8ou', $${
  "id": "p8w2m5zr7c",
  "name": "=== gen8ou Wall of Water ===",
  "gen": "gen8", "tier": "ou",
  "members": [
    {"name": "toxapex", "item": "black sludge", "ability": "regenerator", "nature": "bold",
     "evs": {"hp": 252, "def": 252, "spd": 4},
     "moves": [
       {"scald":   {"name": "scald",   "type": "water",  "priority": 0, "power": 80,   "genre": "special"}},
       {"toxic":   {"name": "toxic",   "type": "poison", "priority": 0, "power": null, "genre": "status"}},
       {"recover": {"name": "recover", "type": "normal", "priority": 0, "power": null, "genre": "status"}},
       {"haze":    {"name": "haze",    "type": "ice",    "priority": 0, "power": null, "genre": "status"}}
     ],
     "type": ["poison", "water"], "dex": 748,
     "spriteUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/748.png",
     "itemUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/black-sludge.png"},
    {"name": "corviknight", "item": "leftovers", "ability": "pressure", "nature": "impish",
     "evs": {"hp": 252, "def": 168, "spd": 88},
     "moves": [
       {"brave-bird": {"name": "brave-bird", "type": "flying", "priority": 0, "power": 120,  "genre": "physical"}},
       {"roost":      {"name": "roost",      "type": "flying", "priority": 0, "power": null, "genre": "status"}},
       {"defog":      {"name": "defog",      "type": "flying", "priority": 0, "power": null, "genre": "status"}},
       {"u-turn":     {"name": "u-turn",     "type": "bug",    "priority": 0, "power": 70,   "genre": "physical"}}
     ],
     "type": ["flying", "steel"], "dex": 823,
     "spriteUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/823.png",
     "itemUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/leftovers.png"},
    {"name": "clefable", "item": "leftovers", "ability": "magic guard", "nature": "calm",
     "evs": {"hp": 252, "def": 4, "spd": 252},
     "moves": [
       {"moonblast":   {"name": "moonblast",   "type": "fairy",   "priority": 0, "power": 95,   "genre": "special"}},
       {"soft-boiled": {"name": "soft-boiled", "type": "normal",  "priority": 0, "power": null, "genre": "status"}},
       {"calm-mind":   {"name": "calm-mind",   "type": "psychic", "priority": 0, "power": null, "genre": "status"}},
       {"flamethrower":{"name": "flamethrower","type": "fire",    "priority": 0, "power": 90,   "genre": "special"}}
     ],
     "type": ["fairy"], "dex": 36,
     "spriteUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/36.png",
     "itemUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/leftovers.png"}
  ]
}$$::jsonb
FROM users WHERE username = 'misty_w';

-- Brock: Gen 4 OU
INSERT INTO teams (user_id, tier, data)
SELECT id, 'gen4ou', $${
  "id": "t4r6n1yd9e",
  "name": "=== gen4ou Sand and Steel ===",
  "gen": "gen4", "tier": "ou",
  "members": [
    {"name": "tyranitar", "item": "choice band", "ability": "sand stream", "nature": "adamant",
     "evs": {"hp": 136, "atk": 252, "spe": 120},
     "moves": [
       {"stone-edge": {"name": "stone-edge", "type": "rock",   "priority": 0, "power": 100, "genre": "physical"}},
       {"crunch":     {"name": "crunch",     "type": "dark",   "priority": 0, "power": 80,  "genre": "physical"}},
       {"pursuit":    {"name": "pursuit",    "type": "dark",   "priority": 0, "power": 40,  "genre": "physical"}},
       {"earthquake": {"name": "earthquake", "type": "ground", "priority": 0, "power": 100, "genre": "physical"}}
     ],
     "type": ["rock", "dark"], "dex": 248,
     "spriteUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/248.png",
     "itemUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/choice-band.png"},
    {"name": "metagross", "item": "life orb", "ability": "clear body", "nature": "adamant",
     "evs": {"hp": 4, "atk": 252, "spe": 252},
     "moves": [
       {"meteor-mash":  {"name": "meteor-mash",  "type": "steel",  "priority": 0, "power": 90,  "genre": "physical"}},
       {"earthquake":   {"name": "earthquake",   "type": "ground", "priority": 0, "power": 100, "genre": "physical"}},
       {"bullet-punch": {"name": "bullet-punch", "type": "steel",  "priority": 1, "power": 40,  "genre": "physical"}},
       {"explosion":    {"name": "explosion",    "type": "normal", "priority": 0, "power": 250, "genre": "physical"}}
     ],
     "type": ["steel", "psychic"], "dex": 376,
     "spriteUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/376.png",
     "itemUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/life-orb.png"},
    {"name": "starmie", "item": "life orb", "ability": "natural cure", "nature": "timid",
     "evs": {"spa": 252, "spd": 4, "spe": 252},
     "moves": [
       {"surf":         {"name": "surf",         "type": "water",    "priority": 0, "power": 90, "genre": "special"}},
       {"thunderbolt":  {"name": "thunderbolt",  "type": "electric", "priority": 0, "power": 90, "genre": "special"}},
       {"ice-beam":     {"name": "ice-beam",     "type": "ice",      "priority": 0, "power": 90, "genre": "special"}},
       {"rapid-spin":   {"name": "rapid-spin",   "type": "normal",   "priority": 0, "power": 50, "genre": "physical"}}
     ],
     "type": ["water", "psychic"], "dex": 121,
     "spriteUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/121.png",
     "itemUrl": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/life-orb.png"}
  ]
}$$::jsonb
FROM users WHERE username = 'brock_h';

COMMIT;