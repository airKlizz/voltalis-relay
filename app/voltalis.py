import requests


class Voltalis():

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.login()
        self.set_site_id()
        self.set_appliances()

    def login(self):
        json_data = {
            "login": self.username,
            "password": self.password,
        }
        response = requests.post(
            "https://api.myvoltalis.com/auth/login", json=json_data)
        if not response.ok:
            raise ValueError("credentials not valid")
        self.token = response.json()["token"]

    def put(self, url: str, data: dict):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",

        }
        response = requests.put(url, headers=headers, json=data)
        if not response.ok:
            self.login()
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }
            response = requests.put(url, headers=headers)
            if not response.ok:
                raise ValueError("post request unknown error",
                                 response.content)
        return response

    def get(self, url: str):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {self.token}",
        }
        response = requests.get(url, headers=headers)
        if not response.ok:
            self.login()
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Authorization": f"Bearer {self.token}",
            }
            response = requests.get(url, headers=headers)
            if not response.ok:
                raise ValueError("get request unknown error", response.content)
        return response

    def set_site_id(self):
        response = self.get("https://api.myvoltalis.com/api/account/me").json()
        self.site_id = response["defaultSite"]["id"]

    def set_appliances(self):
        if self.site_id == None:
            self.set_site_id()
        response = self.get(
            f"https://api.myvoltalis.com/api/site/{self.site_id}/managed-appliance").json()
        self.appliances = [r["name"] for r in response]
        self.appliances_info = {
            r["name"]: {
                "id": r["id"],
                "is_on": r["programming"]["isOn"],
                "mode": r["programming"]["mode"],
                "available_modes": r["availableModes"],
                "manual_setting_id": r["programming"]["idManualSetting"]
            }
            for r in response}

    def change_applicance_mode(self, appliance: str, mode: str):
        if self.site_id == None:
            self.set_site_id()
        if appliance not in self.appliances:
            raise ValueError(
                f"appliance {appliance} not available. Should be one of {self.appliances}")
        if mode not in self.appliances_info[appliance]["available_modes"]:
            raise ValueError(
                f"mode {mode} not available. Should be one of {self.appliances_info[appliance]['available_modes']}")
        data = {
            "enabled": True,
            "idAppliance": self.appliances_info[appliance]["id"],
            "untilFurtherNotice": True,
            "isOn": True,
            "mode": mode,
            "endDate": None,
        }
        self.put(
            f"https://api.myvoltalis.com/api/site/{self.site_id}/manualsetting/{self.appliances_info[appliance]['manual_setting_id']}", data)
