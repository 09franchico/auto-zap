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
                    "primary": f"#117224",
                },
                "[light]": {
                    "primary": f"#117224",
                },
            },
            additional_qss=qss
        )

    def getTheme(self):
        return qdarktheme.get_themes()
    
    

