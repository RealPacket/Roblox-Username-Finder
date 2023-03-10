from os import chmod

import flet as ft

from cryptography.fernet import Fernet
from Utils.Managers.Account import AccountDB, AccountManager, Path
from Utils.TabComponents.CSniperTab import CSniper
from Utils.TabComponents.CAccountMgr import CAccMgr

key_file_name: str = "[DON'T SHARE OR SHOW TO OTHERS!!!] key.key"
key_file: Path = Path(f"{Path.cwd()}\\{key_file_name}")

if not key_file.exists():
    key = Fernet.generate_key()
    # Write key to file
    with open(key_file_name, "wb") as f:
        f.write(key)
        chmod(key_file_name, 0o600)  # Set file permissions to read-write for owner only
else:
    with open(key_file_name, "rb") as f:
        key = f.read()

# Create an AccountDB instance with the key
ADB = AccountDB(Path("Accounts.db"), key)
AccountMgr = AccountManager(ADB)


def main(page: ft.Page):
    page.title = "Roblox Username Sniper"
    Sniper_tab = ft.Tab(
        text="Sniper",
        content=ft.Container(
            content=ft.Text("Not yet...")
        )
    )
    CSniper(Sniper_tab)
    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            Sniper_tab,
            ft.Tab(
                text="Account Manager",
                content=CAccMgr(AccountMgr).getComp(),
                icon=ft.icons.ACCOUNT_CIRCLE_ROUNDED
            ),
        ],
        expand=1,
    )

    page.add(t)


if __name__ == '__main__':
    print("hi")

ft.app(target=main)
