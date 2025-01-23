import qdarktheme

#pyinstaller --onefile --noconsole main.py 

qss = """
QPushButton {
    
}
"""

class SetupTheme:

    def setupTheme(self,theme):
        qdarktheme.setup_theme(
            theme=theme,
            corner_shape='rounded',
            custom_colors={
                "[dark]": {
                    "primary": f"#0C6DDB",
                },
                "[light]": {
                    "primary": f"#0C6DDB",
                },
            },
            additional_qss=qss
        )

    def getTheme(self):
        return qdarktheme.get_themes()
    
    

