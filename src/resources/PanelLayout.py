from rich.layout import Layout


class PanelLayout:
    """Define panel layout"""

    @classmethod
    def make_layout(self, start: bool) -> Layout:
        """Makes the layout"""
        if not start:
            layout = Layout(name="root")

            layout.split_row(
                Layout(name="main", ratio=6),
                Layout(name="tree", ratio=2),
            )

            layout['main'].split_column(
                Layout(name='main_game', ratio=7),
                Layout(name='footer', ratio=2)
            )
            layout['footer'].split_row(
                Layout(name='Other_info', ratio=7),
                Layout(name='inventory', ratio=3)
            )
        else:
            layout = Layout(name="start")

        return layout
