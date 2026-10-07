import random
import time
from typing import Any, Dict, Optional

import requests
from urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#  https://api.alldragon.com/msite/wxxcx/getXcxSessionToken.json
token_list = [

    {
        "name": "heart_beats",
        "token": "df1c188673ba4c85b2361a9f57c02748",
    },
]


# env_url 来自小程序 extConfig 里的 env_url。
# 接口最终会拼成：https://api.{ENV_URL}/msite/loginByToken.json
# 例如如果抓包看到域名是 https://api.example.com/mkt2/checkin/checkin.json，
# 这里就填 example.com。
ENV_URL = "alldragon.com"

TENANT_ID = "4202"
TENANT_CODE = "lyqs"
CLIENT_TYPE = 3
VERIFY_SSL = False


# 这里的 token 是 wxSessionInfo.session_token，不是 Authorization。
# 也就是 /msite/wxxcx/getXcxSessionToken.json 返回 data.session_token。



BASE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/132.0.0.0 Safari/537.36 "
        "MicroMessenger/7.0.20.1781 MiniProgramEnv/Windows"
    ),
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Referer": "https://servicewechat.com/",
}


def api_url(service: str, path: str) -> str:
    return f"https://api.{ENV_URL}/{service}{path}"


def common_data() -> Dict[str, Any]:
    return {
        "tenantId": TENANT_ID,
        "tenantCode": TENANT_CODE,
        "clientType": CLIENT_TYPE,
    }


def login_by_token(session: requests.Session, session_token: str) -> Optional[str]:
    data = {
        "token": session_token,
        **common_data(),
    }

    response = session.post(
        api_url("msite", "/loginByToken.json"),
        headers=BASE_HEADERS,
        data=data,
        timeout=15,
        verify=VERIFY_SSL,
    )
    result = response.json()

    if result.get("code") != 200:
        print("loginByToken 失败：")
        print(result)
        return None

    authorization = result.get("data", {}).get("authorization")
    if not authorization:
        print("loginByToken 成功但没有返回 authorization：")
        print(result)
        return None

    return authorization


def checkin(session: requests.Session, authorization: str) -> Dict[str, Any]:
    headers = {
        **BASE_HEADERS,
        "Authorization": authorization,
    }

    response = session.post(
        api_url("mkt2", "/checkin/checkin.json"),
        headers=headers,
        data=common_data(),
        timeout=15,
        verify=VERIFY_SSL,
    )
    return response.json()


def main() -> None:
    if ENV_URL == "请替换成env_url":
        raise SystemExit("请先把 ENV_URL 改成真实 env_url，例如 xxx.com")

    for item in token_list:
        name = item["name"]
        session_token = item["token"]

        delay = random.uniform(3, 10)
        time.sleep(delay)

        print(f"\n{name} 开始登录并签到...")

        try:
            session = requests.Session()
            authorization = login_by_token(session, session_token)
            if not authorization:
                continue

            result = checkin(session, authorization)
            print(f"{name} 签到结果：")
            print(result)

        except Exception as exc:
            print(f"{name} 签到失败：{exc}")


if __name__ == "__main__":
    main()
