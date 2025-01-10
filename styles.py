import qdarktheme


qss = """
QPushButton {
    border-width: 2px;
    border-style: dashed;
    height: 30px;
}
"""

class SetupTheme:

    def setupTheme(self,theme):
        qdarktheme.setup_theme(
            theme=theme,
            corner_shape='rounded',
            custom_colors={
                "[dark]": {
                    "primary": f"#33DC09",
                },
                "[light]": {
                    "primary": f"#33DC09",
                },
            },
            additional_qss=qss
        )

    def getTheme(self):
        return qdarktheme.get_themes()
    
    

