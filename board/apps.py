from django.apps import AppConfig


class BoardConfig(AppConfig):
    name = 'board'
    verbose_name = "게시글 관리"

    def ready(self):
        import board.signals