from apps.common.views import SidebarItem


class SidebarConfig:
    """
    サイドバー項目に関する Config クラス
    """
    questions: list[SidebarItem] = [
        {
            'label': '問題一覧',
            'view_name': 'question_list',
            'icon': 'edit_document',
        },
    ]
