import qdarktheme

#pyinstaller --onedir --noconsole main.py 

qss = """
    QGroupBox[customProperty='highlighted'] {
            font-size: 14px;
            font-weight: normal;
            border-radius: 6px;
            padding: 10px;
        }
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
    
    

