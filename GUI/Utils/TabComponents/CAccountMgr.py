import flet as ft
import flet_core
from Utils.Managers.Account import AccountManager


class CAccMgr:

    def __init__(self, AccMgr: AccountManager):
        self.AccMgr = AccMgr

    def getComp(self):
        AccUsernameDL: [list[flet_core.DataRow]] = []
        for account in self.AccMgr.get_accounts():
            username = account[0]
            password = account[1]
            AccUsernameDL.append(
                ft.DataRow(
                    [ft.DataCell(ft.Text(value=username.decode())), ft.DataCell(ft.Text(value=password.decode()))]
                )
            )
        return ft.Container(
            content=ft.DataTable(
                width=700,
                bgcolor="grey",
                # border=ft.border.all(2, "red"),
                border_radius=10,
                vertical_lines=ft.border.BorderSide(3, "blue"),
                horizontal_lines=ft.border.BorderSide(1, "green"),
                sort_column_index=0,
                sort_ascending=True,
                heading_row_color=ft.colors.BLACK12,
                heading_row_height=100,
                divider_thickness=0,
                column_spacing=200,
                columns=[
                    ft.DataColumn(
                        ft.Text("Username"),
                        tooltip="The username of the accounts"
                    ),
                    ft.DataColumn(
                        ft.Text("Password"),
                        tooltip="The password of the accounts"
                    ),
                ],
                rows=AccUsernameDL
            ),
        )
