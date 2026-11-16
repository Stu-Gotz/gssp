from smog_usage_stats import api, metagame, transformer

import re
import os
import sys
import time
import psycopg2
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta

## AUTHOR'S NOTE
# Things I need to fucking do:
# 1. clean up code. to be more precise, reduce some of the redundancy, probably tidy up the sql functionality
#    and just make it a bit more professional. Also probably stop using "fuck" in comments
# 2. Implement streaming option. Something to the effect of:
#    [source data](get) ->
#    [parse into dataframe (polars?)] ->
#    {load sequentially to db}
# 3. add a CLI function if possible, or (power)shell script


# param_dict something like


# {
#   branch: 'BaseStats', 'MonoStats', 'BaseChaos', 'MonoChaos"
#   year, gen, month, tier or typing all as their own fields
#   isMonotype: True or False
#   }
class Updater:
    # This is finished and optimised a great deal more. Currently runs in about 69-70s
    # Need to add doc strings, remove print statements, clean it up a bit
    # Interested in looking into one of asyncio, multithreading/processing to speed up
    # even further but future me's problem.
    def __init__(self, isMonotype: bool = False):
        self.isMonotype = isMonotype

    @staticmethod
    def _set_query_object(param_dict: dict) -> list[transformer.Usage]:
        """
        Basically a backend router that returns a Search.<subclass> object
        """
        match param_dict["branch"]:
            case "BaseStats":
                new_query = api.usage_stats(
                    metagame.Metagame(
                        year=param_dict["year"],
                        month=param_dict["month"],
                        gen=param_dict["gen"],
                        tier=param_dict["branch_param"],
                    )
                )
                return new_query
            case "MonoStats":
                new_query = api.usage_stats(
                    metagame.Metagame(
                        year=param_dict["year"],
                        month=param_dict["month"],
                        gen=param_dict["gen"],
                        typing=param_dict["branch_param"],
                    )
                )
            case "BaseChaos":
                new_query = api.extended_stats(
                    metagame.Metagame(
                        year=param_dict["year"],
                        month=param_dict["month"],
                        gen=param_dict["gen"],
                        tier=param_dict["branch_param"],
                    )
                )
            case "MonoChaos":
                new_query = api.extended_stats(
                    metagame.Metagame(
                        year=param_dict["year"],
                        month=param_dict["month"],
                        gen=param_dict["gen"],
                        typing=param_dict["branch_param"],
                    )
                )
        return new_query

    @staticmethod
    def _update_database() -> None:
        """Updates the database with new data."""
        sqli = SQLInterface()
        sqli.connect()
        print("Connected!")
        sqli.update_tables()
        for i in ("current", "previous", "tma"):
            sqli.load_data_to_table(i)

        sqli.close_connection()
        print("Database successfully updated.")

    def update_monthly(self) -> None:
        """Called on a monthly basis to update the database as new stats are released."""
        today = datetime.now()

        # realistically, I should only have to need the current data, and then I can
        # just reshuffle the folders with shutil functions, which I will probably
        # change to, but I need to get a working amount of data to work with and have
        # something to fall back on if I somehow delete a bunch of data I cannot get
        # back.
        # I kind of already did this in the old version, so I'll just look there and
        # see how to handle it.

        # ADDITIONAL FUTURE CHANGES:
        #   Include stream to database to skip saving.
        date_dict = {
            "current": today - relativedelta(months=1),
            "previous": today - relativedelta(months=2),
            "tma": today - relativedelta(months=3),
        }

        # gens = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        def get_stats_links(date_obj: datetime) -> tuple[str]:
            """Internal function to get the available tiers to query. Faster than
            iterating as it reduces the number of tiers by only picking from the
            available ones. There's definitely a better way to do this which I am
            going to change to that just uses the anchor tags ending in -1500.txt,
            but at the moment this is good enough for a solution to work on perfecting.

                Params:
                date_obj (datetime): a datetime object of at least YYYY-MM format.

                Returns:
                tuple[str] -> a tuple of tiers, as string values
            """
            year = date_obj.strftime("%Y")
            month = date_obj.strftime("%m")
            url = f"https://www.smogon.com/stats/{year}-{month}/"

            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            anchors = soup.find_all("a")
            available_stats = [
                url + a.text for a in anchors if a.text.endswith("-1500.txt")
            ]
            return available_stats

        def get_data(stats_links: list, table: str, isMonotype: bool = False) -> None:
            """Function to retrieve data from the source, parse it and save an output.

            Params:
                stat_links(list): A list of valid urls of smogon stat's pages
                table(str): A string value of the time period of interest, eg: current for most recent capture.
                isMonotype(bool): Boolean flag to set for monotype search. Default is `False`

            Returns:
                None

            """
            match_pattern = r"gen[0-9]"
            branch = "BaseStats"
            if isMonotype:
                branch = "MonoStats"
            for link in stats_links:
                link = link.removesuffix(
                    "-1500.txt"
                )  # .split matches any inside which was causing errors
                gen = re.search(match_pattern, link).group()
                gen = re.sub(r"[a-z]", "", gen)
                ttier = re.split(match_pattern, link, maxsplit=1)
                # max splits because there is a tier `moderngen2 which fucks it up`
                tier = ttier[-1]
                q = self._set_query_object(
                    {
                        "year": date_dict[table].strftime("%Y"),
                        "month": date_dict[table].strftime("%m"),
                        "gen": gen,
                        "branch_param": tier,
                        "branch": branch,
                        "isMonotype": isMonotype,
                    }
                )
                print(f"Adding target url: {q.base}")
                q.search_and_save(pathname=table)

        # for k in date_dict.keys():
        #     stats_links = get_stats_links(date_dict[k])
        #     get_data(stats_links, table=k, isMonotype=self.isMonotype)

        self._update_database()


_COLUMNS = {
    # "id_": "SERIAL PRIMARY KEY",
    "rank": "INTEGER",
    "pokemon": "VARCHAR(50)",
    "usage_pct": "FLOAT",
    "raw_usage": "INTEGER",
    "raw_pct": "FLOAT",
    "real": "INTEGER",
    "real_pct": "FLOAT",
    "date": "VARCHAR(50)",
    "tier": "VARCHAR(50)",
}


class SQLInterface:
    def __init__(
        self,
        db_name: str = None,
        username: str = None,
        pwd: str = None,
        host: str = None,
        port: str = None,
    ) -> None:
        self.db_name = db_name if db_name else os.environ.get("LOCAL_DATABASE")
        self.username = username if username else os.environ.get("LOCAL_USER")
        self.pwd = pwd if pwd else os.environ.get("LOCAL_PASS")
        self.host = host if host else os.environ.get("LOCAL_HOST")
        self.port = port if host else os.environ.get("LOCAL_PORT}")

        self.conn = self.connect(
            database=self.db_name,
            user=self.username,
            password=self.pwd,
            host=self.host,
            port=self.port,
        )

    def connect(
        self,
        database: str = None,
        user: str = None,
        password: str = None,
        host: str = None,
        port: str = None,
    ) -> psycopg2.extensions.connection:
        """ """
        connection = psycopg2.connect(
            database=database if database else os.environ.get("LOCAL_DATABASE"),
            user=user if user else os.environ.get("LOCAL_USER"),
            password=password if password else os.environ.get("LOCAL_PASS"),
            host=host if host else os.environ.get("LOCAL_HOST"),
            port=port if host else os.environ.get("LOCAL_PORT"),
        )

        if connection:
            self.conn = connection
            print(f"Connected to {database}.")
        else:
            raise ConnectionError(
                "No database connection was established. Please check your credentials."
            )

        return connection

    def _create_cursor(self) -> psycopg2.extensions.cursor:
        """
        If the user hasn't connected manually, no self.conn exists, so we must call it and create the cursor from default values.

        This function is here because its good practice to close the cursor after executing a command. So it is called at the top of a
        SQL-performing function and closed after it.
        """
        if not self.conn:
            self.conn = self.connect()
        curr = self.conn.cursor()
        return curr

    def update_tables(self) -> None:
        db_names = ("current", "previous", "tma")
        columns = ",\n".join(f"{k} {v}" for k, v in _COLUMNS.items())

        cursor = self._create_cursor()

        sql_cmd = f"DROP TABLE IF EXISTS {db_names[-1]}; \n"
        sql_cmd += f"DROP TABLE IF EXISTS {db_names[1]};\n"
        sql_cmd += f"DROP TABLE IF EXISTS {db_names[0]};\n"
        sql_cmd += f"CREATE TABLE {db_names[0]} ({columns});\n"
        sql_cmd += f"CREATE TABLE {db_names[1]} ({columns});\n"
        sql_cmd += f"CREATE TABLE {db_names[-1]} ({columns});\n"

        cursor.execute(sql_cmd)
        self.conn.commit()
        self._close_cursor(cursor)
        return

    def load_data_to_table(self, target_table: str) -> None:
        cursor = self._create_cursor()

        for source in os.listdir(target_table):
            with open(os.path.join(target_table, source), "r") as truth:
                next(truth)
                cursor.copy_from(truth, target_table, columns=_COLUMNS, sep=",")
                self.conn.commit()
        self._close_cursor(cursor)

    def close_connection(self) -> None:
        """Closes database connection."""
        self.conn.close()

    def _close_cursor(self, cursor: psycopg2.extensions.cursor) -> None:
        """Closes cursor."""
        cursor.close()


if __name__ == "__main__":
    load_dotenv(dotenv_path=".env")

    # Updater().update_monthly()
    # if sys.argv[0] is None or sys.argv[0] == "output":
    #     start = time.time()
    #     try:
    #         Updater().update_monthly()
    #     except ValueError:
    #         end = time.time()
    #         print(f"Process failed. Elapsed time: {end - start}")

    #     print(f"Process complete. Elapsed time: {time.time() - start}")
    #     exit(1)
    # elif sys.argv[0] == "stream":
    #     print("Implement streaming you lazy jackass.")
    #     pass

    ##### THIS IS ALL JUST TESTING AND FOR TESTING NEW FEATURES STUFF IF IT WORKS

    sqli = SQLInterface()
    # sqli.update_tables()
    # gotta do the dirlist and pass the current, previous, tma dirs and tables
    # tables = ["current", "previous", "tma"]
    # [sqli.load_data_to_table(target_table=t) for t in tables]
    # sqli.close_connection()

    # def get_tiers():  # date_obj: datetime) -> tuple[str]:
    #     """Internal function to get the available tiers to query. Faster than
    #     iterating as it reduces the number of tiers by only picking from the
    #     available ones. There's definitely a better way to do this which I am
    #     going to change to that just uses the anchor tags ending in -1500.txt,
    #     but at the moment this is good enough for a solution to work on perfecting.

    #         Params:
    #         date_object (datetime): a datetime object of at least YYYY-MM format

    #         Returns:
    #         tuple[str] -> a tuple of tiers, as string values
    #     """
    #     # year = date_obj.strftime("%Y")
    #     # month = date_obj.strftime("%m")
    #     url = f"https://www.smogon.com/stats/2024-07/"

    #     r = requests.get(url)
    #     soup = BeautifulSoup(r.text, "html.parser")
    #     anchors = soup.find_all("a")
    #     good_urls = [url + a.text for a in anchors if a.text.endswith("-1500.txt")]
    #     print(good_urls)

    # get_tiers()

    # if __name__ == "__main__":
    # gen_pattern = r"(gen[0-9])"
    # link = "https://www.smogon.com/stats/2024-07/gen71v1-1500.txt"
    # # tier = re.split(r"gen[0-9]", link)[-1]
    # gen = re.search(gen_pattern, link).group()
    # gen = re.sub(r'[a-z]', '', gen)
    # # gen = gen.replace(r'[a-z]', '')
    # print(gen)
    # import json
    # import os
    # import re

    # import psycopg2

    # CREATE_TABLE_SQL = """
    # CREATE TABLE IF NOT EXISTS pokedex (
    # id           TEXT PRIMARY KEY,         -- showdown id, e.g. 'greattusk'
    # num          INTEGER NOT NULL,         -- national dex number (shared by formes)
    # name         TEXT NOT NULL UNIQUE,     -- 'great tusk'
    # base_species TEXT,
    # forme        TEXT,
    # types        TEXT[] NOT NULL,
    # hp INTEGER, atk INTEGER, def INTEGER, spa INTEGER, spd INTEGER, spe INTEGER,
    # abilities    JSONB,
    # heightm      REAL,
    # weightkg     REAL,
    # prevo        TEXT,
    # evos         TEXT[],
    # egg_groups   TEXT[],
    # other_formes TEXT[],
    # extra        JSONB NOT NULL DEFAULT '{}'
    # );
    # CREATE INDEX IF NOT EXISTS pokedex_num_idx ON pokedex (num);
    # """

    # # Keys that get their own column; everything else goes into "extra".
    # CORE_COLUMNS = {
    #     "num",
    #     "name",
    #     "base_species",
    #     "forme",
    #     "types",
    #     "abilities",
    #     "heightm",
    #     "weightkg",
    #     "prevo",
    #     "evos",
    #     "egg_groups",
    #     "other_formes",
    # }
    # STAT_COLUMNS = ["hp", "atk", "def", "spa", "spd", "spe"]
    # ALL_COLUMNS = ["id", *sorted(CORE_COLUMNS), *STAT_COLUMNS, "extra"]

    # def _snake(key):
    #     """baseStats -> base_stats, eggGroups -> egg_groups."""
    #     return re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", key).lower()

    # def _lower(value):
    #     """Lower-case (and trim) every string, including inside nested dicts and lists."""
    #     if isinstance(value, str):
    #         return value.strip().lower()
    #     if isinstance(value, dict):
    #         return {_lower(k): _lower(v) for k, v in value.items()}
    #     if isinstance(value, list):
    #         return [_lower(v) for v in value]
    #     return value

    # def insert_pokedex(cursor, payload):
    #     """Upsert every real Pokémon in payload["data"]; returns the row count."""
    #     rows = []
    #     for showdown_id, entry in payload["data"].items():
    #         entry = {_snake(k): _lower(v) for k, v in entry.items()}
    #         if entry.get("num", 0) <= 0:  # CAP, Pokestar, MissingNo, cosmetic formes
    #             continue

    #         stats = entry.pop("base_stats", {})
    #         row = {"id": showdown_id.lower(), "extra": {}}
    #         for key, value in entry.items():
    #             if key in CORE_COLUMNS:
    #                 row[key] = value
    #             else:
    #                 row["extra"][key] = value
    #         for stat in STAT_COLUMNS:
    #             row[stat] = stats.get(stat)

    #         rows.append(
    #             [
    #                 json.dumps(row.get(c))
    #                 if isinstance(row.get(c), dict)
    #                 else row.get(c)
    #                 for c in ALL_COLUMNS
    #             ]
    #         )

    #     column_sql = ", ".join(f'"{c}"' for c in ALL_COLUMNS)
    #     placeholders = ", ".join(["%s"] * len(ALL_COLUMNS))
    #     updates = ", ".join(f'"{c}" = EXCLUDED."{c}"' for c in ALL_COLUMNS if c != "id")
    #     cursor.executemany(
    #         f"INSERT INTO pokedex ({column_sql}) VALUES ({placeholders}) "
    #         f"ON CONFLICT (id) DO UPDATE SET {updates}",
    #         rows,
    #     )
    #     return len(rows)

    # with open(os.path.join(os.getcwd(), "backend/assets/smogdex.json")) as f:
    #     payload = json.load(f)

    # connection = psycopg2.connect(
    #     database=os.environ.get("LOCAL_DATABASE"),
    #     user=os.environ.get("LOCAL_USER"),
    #     password=os.environ.get("LOCAL_PASS"),
    #     host=os.environ.get("LOCAL_HOST"),
    #     port=os.environ.get("LOCAL_PORT"),
    # )
    # try:
    #     with connection:  # commits on success, rolls back on error
    #         with connection.cursor() as cur:
    #             cur.execute(CREATE_TABLE_SQL)
    #             connection.commit()
    #             count = insert_pokedex(cur, payload)
    #     print(f"Upserted {count} Pokémon")
    # finally:
    #     connection.close()

    # import json
    # import os

    # import psycopg2
    # import requests

    # from backend.api.utils import to_id  # wherever you put to_id

    # OVERRIDES_PATH = "backend/assets/name_map.json"

    # def load_pokeapi_by_id():
    #     resp = requests.get(
    #         "https://pokeapi.co/api/v2/pokemon", params={"limit": 100000}, timeout=30
    #     )
    #     resp.raise_for_status()
    #     names = [p["name"] for p in resp.json()["results"]]
    #     return {to_id(name): name for name in names}, set(names)

    # def main():
    #     with open(OVERRIDES_PATH) as f:
    #         overrides = json.load(f)
    #     manual = overrides["pokemon"]
    #     form_only = set(overrides["form_only"])

    #     pokeapi_by_id, pokeapi_names = load_pokeapi_by_id()

    #     # Catch typos in the overrides file before touching the database.
    #     bad = {k: v for k, v in manual.items() if v not in pokeapi_names}
    #     if bad:
    #         raise SystemExit(f"Overrides that don't exist in PokeAPI: {bad}")

    #     connection = psycopg2.connect(
    #         database=os.environ.get("LOCAL_DATABASE"),
    #         user=os.environ.get("LOCAL_USER"),
    #         password=os.environ.get("LOCAL_PASS"),
    #         host=os.environ.get("LOCAL_HOST"),
    #         port=os.environ.get("LOCAL_PORT"),
    #     )
    #     try:
    #         with connection:
    #             with connection.cursor() as cur:
    #                 cur.execute(
    #                     "ALTER TABLE pokedex ADD COLUMN IF NOT EXISTS pokeapi_slug TEXT"
    #                 )
    #                 cur.execute("SELECT id FROM pokedex")
    #                 ids = [row[0] for row in cur.fetchall()]

    #                 updates, unmatched = [], []
    #                 for showdown_id in ids:
    #                     slug = manual.get(showdown_id) or pokeapi_by_id.get(showdown_id)
    #                     if slug:
    #                         updates.append((slug, showdown_id))
    #                     elif showdown_id not in form_only:
    #                         unmatched.append(showdown_id)

    #                 cur.executemany(
    #                     "UPDATE pokedex SET pokeapi_slug = %s WHERE id = %s", updates
    #                 )

    #         print(f"Set pokeapi_slug on {len(updates)} of {len(ids)} rows")
    #         if unmatched:
    #             print(f"Unmatched ({len(unmatched)}): {', '.join(sorted(unmatched))}")
    #     finally:
    #         connection.close()

    # main()
