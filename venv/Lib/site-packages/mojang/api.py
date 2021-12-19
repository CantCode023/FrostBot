"""
The MIT License (MIT)

Copyright (c) 2021 https://github.com/summer

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import ast
import base64
import logging
import json
from typing import Optional

import requests

from .models import UserProfile


log = logging.getLogger(__name__)


class MojangError(Exception):
    """Base error class for all library-related exceptions in this file
    Essentially, this could be caught to handle any exceptions thrown from this library.
    """

    def __init__(self, message: Optional[str] = None):
        self.message = message if message else self.__class__.__doc__
        super().__init__(self.message)


class MojangAPI:
    @staticmethod
    def get_uuid(username: str, timestamp: int = None) -> Optional[str]:
        """Convert a Minecraft name to a UUID.

        Error: Limited Functionality
            As of November 2020, Mojang stopped supporting the timestamp parameter, which allowed
            users to get UUID of the name at the timestamp provided. If a timestamp is provided,
            it is silently ignored and the current UUID is returned. Please remind them to fix this here:
            [WEB-3367](https://bugs.mojang.com/browse/WEB-3367).

        Args:
            username:  The Minecraft username to be converted.
            timestamp (optional): Get the username's UUID at a specified UNIX timestamp.
                You can also get the username's first UUID by passing `0` to this parameter.
                However, this only works if the name was changed at least once, or if the account is legacy.

        Returns:
            The UUID (`str`) or `None` if the username does not exist.

        Example:
            ```py
            uuid = MojangAPI.get_uuid("Notch")

            if not uuid:
                print("The username Notch is not taken")
            else:
                print(f"Notch's UUID is {uuid}")
            ```
        """

        if timestamp:
            resp = requests.get(
                f"https://api.mojang.com/users/profiles/minecraft/{username}?at={timestamp}"
            )
        else:
            resp = requests.get(
                f"https://api.mojang.com/users/profiles/minecraft/{username}"
            )

        if not resp.ok:
            return None

        try:
            return resp.json()["id"]
        except json.decoder.JSONDecodeError:
            return None

    @staticmethod
    def get_uuids(names: list) -> dict:
        """Convert up to 10 usernames to UUIDs in a single network request.

        Args:
            names: The Minecraft username(s) to be converted.
                If more than 10 are included, only the first 10 will be parsed.

        Returns:
            A dictionary object that contains the converted usernames. Names are also case-corrected.
            If a username does not exist, it will not be included in the returned dictionary.

        Example:
            ```py
            usernames = ["Notch", "Herobrine", "Dream"]

            players = MojangAPI.get_uuids(usernames)

            for name, uuid in players.items():
                print(name, uuid)
            ```
        """
        if len(names) > 10:
            names = names[:10]
        data = requests.post(
            "https://api.mojang.com/profiles/minecraft", json=names
        ).json()

        if not isinstance(data, list):
            if data.get("error"):
                raise ValueError(data["errorMessage"])
            else:
                raise MojangError(data)

        sorted_names = dict()
        for name_data in data:
            sorted_names[name_data["name"]] = name_data["id"]

        return sorted_names

    @staticmethod
    def get_username(uuid: str) -> Optional[str]:
        """Convert a UUID to a username.

        Args:
            uuid: The Minecraft UUID to be converted to a username.

        Returns:
            The username. `None` otherwise.

        Example:
            ```py
            username = MojangAPI.get_username("e149b689-d25c-4ace-a9ea-4be1e8407f85")

            if not username:
                print("UUID does not appear to be valid.")
            ```
        """
        resp = requests.get(
            f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        )
        if resp.ok:
            try:
                return resp.json()["name"]
            except json.decoder.JSONDecodeError:
                return None
        return None

    @staticmethod
    def get_profile(uuid: str) -> Optional[UserProfile]:
        """Get more information about a user from their UUID

        Args:
            uuid: The Minecraft UUID

        Returns:
            `UserProfile` object. Otherwise, `None` if the profile does not exist.

        Example:
            ```py
            uuid = MojangAPI.get_uuid("Notch")

            if uuid:
                profile = MojangAPI.get_profile(uuid)

                print(profile.name)
                print(profile.skin_url)
                # other possible profile attributes include skin_model, cape_url,
                # is_legacy_profile, and timestamp
            ```
        """
        resp = requests.get(
            f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        )

        try:
            value = resp.json()["properties"][0]["value"]
        except (KeyError, json.decoder.JSONDecodeError):
            return None
        user_profile = ast.literal_eval(base64.b64decode(value).decode())
        return UserProfile(user_profile)

    @staticmethod
    def get_name_history(uuid: str) -> list:
        """Get a user's name history

        Args:
            uuid: The user's UUID.

        Returns:
            A list of dictionaries, each of which contains a name:changed_to_at pair.
                If changed_to_at is set to 0, it is because it is the profile's first name.

        Example:
            ```py
            uuid = MojangAPI.get_uuid("Dream")

            name_history = MojangAPI.get_name_history(uuid)

            for data in name_history:
                if data['changed_to_at'] == 0:
                    print(f"{data['name']} was the user's first name")
                else:
                    print(f"{uuid} had the name {data['name']} on {data['changed_to_at']}")
            ```
        """
        name_history = requests.get(
            f"https://api.mojang.com/user/profiles/{uuid}/names"
        ).json()

        name_data = list()
        for data in name_history:
            name_data_dict = dict()
            name_data_dict["name"] = data["name"]
            if data.get("changedToAt"):
                name_data_dict["changed_to_at"] = data["changedToAt"]
            else:
                name_data_dict["changed_to_at"] = 0
            name_data.append(name_data_dict)
        return name_data

    @staticmethod
    def get_api_status() -> dict:
        """Get the network status of various Mojang services and API endpoints

        Returns:
            A dictionary object that contains the status of various Mojang services.
            Possible values are green (no issues), yellow (some issues), red (service unavailable).

        Example:
        ```py
        data = MojangAPI.get_api_status()

        for server, status in data.items():
            if status == "red":
                print(f"{server} is down right now.")
            else:
                print(f"{server} is alive and healthy!")
        ```
        """
        data = requests.get("https://status.mojang.com/check").json()
        servers = dict()
        for server_data in data:
            for k, v in server_data.items():
                servers[k] = v
        return servers

    @staticmethod
    def get_blocked_servers() -> list:
        """Get a list of SHA1 hashes of blacklisted Minecraft servers that do not follow EULA.
        These servers have to abide by the EULA or they will be shut down forever. The hashes are not cracked.

        Returns:
            Blacklisted server hashes

        Example:
        ```py
        servers = MojangAPI.get_blocked_servers()

        for hash in servers:
            print(hash)
        ```
        """
        return requests.get(
            "https://sessionserver.mojang.com/blockedservers"
        ).text.splitlines()

    @staticmethod
    def get_sale_statistics(
        item_sold_minecraft: bool = True,
        prepaid_card_redeemed_minecraft: bool = True,
        item_sold_cobalt: bool = False,
        item_sold_scrolls: bool = False,
        prepaid_card_redeemed_cobalt: bool = False,
        item_sold_dungeons: bool = False,
    ) -> dict:
        """Get statistics on the sales of Minecraft.
        You will receive a single object corresponding to the sum of sales of the requested type(s)
        At least one type of sale must be set to True.

        Returns:
            The sales metrics. Possible keys include `total`, `last24h` and `sale_velocity_per_seconds`

        Example:
            ```py
            kwargs = dict(item_sold_minecraft=True,
                          prepaid_card_redeemed_minecraft=True,
                          item_sold_cobalt=False,
                          item_sold_scrolls=False,
                          prepaid_card_redeemed_cobalt=False,
                          item_sold_dungeons=False
                          )

            metrics = MojangAPI.get_sale_statistics(**kwargs)

            print(metrics["total"])
            print(metrics["last24h"])
            print(metrics["sale_velocity_per_seconds"])
            ```
        """
        options = [k for k, v in locals().items() if v]

        if not options:
            raise MojangError(
                "Invalid parameters supplied. Include at least one metric key."
            )

        data = requests.post(
            "https://api.mojang.com/orders/statistics", json={"metricKeys": options}
        ).json()
        metrics = dict()
        metrics["total"] = data["total"]
        metrics["last24h"] = data["last24h"]
        metrics["sale_velocity_per_seconds"] = data["saleVelocityPerSeconds"]
        return metrics

    @staticmethod
    def refresh_access_token(access_token: str, client_token: str) -> dict:
        """Refreshes access token

        Args:
            access_token: The access token to refresh.
            client_token: The client token that was used to obtain the access token.

        Returns:
            A dictionary object that contains the new access token and other account and profile information

        Example:
            ```py
            access_token = "YOUR_ACCESS_TOKEN"
            client_token = "YOUR_CLIENT_TOKEN"

            account = MojangAPI.refresh_access_token(access_token, client_token)

            print("The new access token is " + account["access_token"])

            # main keys include...
            print(account["access_token"])
            print(account["client_token"])
            print(account["username"])
            print(account["uuid"])

            # these will only be populated if the account has a Minecraft profile
            print(account["profile_id"])
            print(account["profile_name"])
            ```
        """
        payload = {
            "accessToken": access_token,
            "clientToken": client_token,
            "requestUser": True,
        }

        account = dict()
        data = requests.post(
            "https://authserver.mojang.com/refresh", json=payload
        ).json()

        account["username"] = data["user"]["username"]
        account["uuid"] = data["user"]["id"]
        account["access_token"] = data["accessToken"]
        account["client_token"] = data["clientToken"]
        if data.get("selectedProfile"):
            account["profile_id"] = data["selectedProfile"]["id"]
            account["profile_name"] = data["selectedProfile"]["name"]
        else:
            account["profile_id"] = None
            account["profile_name"] = None
        return account
