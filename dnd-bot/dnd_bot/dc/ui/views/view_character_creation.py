import nextcord


class ModalNameForm(nextcord.ui.Modal):
    """First form in character creation process"""
    def __init__(self):
        super().__init__("Name Form")

        self.name_textbox = nextcord.ui.TextInput(
            label="Name",
            placeholder="Enter your character name!",
        )

        self.backstory_textbox = nextcord.ui.TextInput(
            label="Background",
            placeholder="Tell something about your past!"
        )

        self.add_item(self.name_textbox)
        self.add_item(self.backstory_textbox)
