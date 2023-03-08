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

    # TODO handle callback function
    async def callback(self, interaction: nextcord.Interaction):
        pass


class ViewAlignmentForm(nextcord.ui.View):
    """View with dropdowns for two axes of alignment"""
    def __init__(self):
        super().__init__()

        lawfulness_option1 = nextcord.SelectOption(
            label="Lawful",
            description="You're honorable man and you like to follow the rules.",
            emoji="📜")

        lawfulness_option2 = nextcord.SelectOption(
            label="Neutral",
            description="You're not a rebel but rules are not sacred to you.",
            emoji="⚖")

        lawfulness_option3 = nextcord.SelectOption(
            label="Chaotic",
            description="You are a free man and you bow to no one.",
            emoji="🤪")

        self.lawfulness_axis_dropdown = nextcord.ui.Select(
            placeholder="Law VS Chaos",
            options=[lawfulness_option1, lawfulness_option2, lawfulness_option3],
            row=0)

        goodness_option1 = nextcord.SelectOption(
            label="Good",
            description="Your altruism is beyond the scale.",
            emoji="👼")

        goodness_option2 = nextcord.SelectOption(
            label="Neutral",
            description="You don't kill the innocent neither you risk life for them.",
            emoji="😐")

        goodness_option3 = nextcord.SelectOption(
            label="Evil",
            description="You would sell your own mother with a smile on your face.",
            emoji="😈")

        self.goodness_axis_dropdown = nextcord.ui.Select(
            placeholder="Good VS Evil",
            options=[goodness_option1, goodness_option2, goodness_option3],
            row=1)

        self.add_item(self.lawfulness_axis_dropdown)
        self.add_item(self.goodness_axis_dropdown)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red, row=2)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass

    # TODO handle next and back buttons callbacks
    @nextcord.ui.button(label='Next', style=nextcord.ButtonStyle.green, row=2)
    async def next(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass


class ViewClassForm(nextcord.ui.View):
    """View with dropdown for selecting a class"""
    def __init__(self):
        super().__init__()

        class_option1 = nextcord.SelectOption(
            label="Warrior",
            description="You like close encounters with your enemies.",
            emoji="⚔")

        class_option2 = nextcord.SelectOption(
            label="Mage",
            description="You're a magic freak.",
            emoji="🧙")

        class_option3 = nextcord.SelectOption(
            label="Ranger",
            description="Bow is your closest friend.",
            emoji="🏹")

        self.class_dropdown = nextcord.ui.Select(
            placeholder="Select a class.",
            options=[class_option1, class_option2, class_option3],
            row=0)

        self.add_item(self.class_dropdown)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red, row=1)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass

    # TODO handle next and back buttons callbacks
    @nextcord.ui.button(label='Next', style=nextcord.ButtonStyle.green, row=1)
    async def next(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass


class ViewRaceForm(nextcord.ui.View):
    """View with dropdown for selecting a race"""
    def __init__(self):
        super().__init__()

        race_option1 = nextcord.SelectOption(
            label="Human",
            description="Just ordinary Adam's offspring.",
            emoji="👨")

        race_option2 = nextcord.SelectOption(
            label="Elf",
            description="You have a lot of grace.",
            emoji="🧝")

        race_option3 = nextcord.SelectOption(
            label="Dwarf",
            description="You're a rough hard worker.",
            emoji="🤏")

        self.race_dropdown = nextcord.ui.Select(
            placeholder="Select a race.",
            options=[race_option1, race_option2, race_option3],
            row=0)

        self.add_item(self.race_dropdown)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red, row=1)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass

    # TODO handle confirm and back buttons callbacks
    @nextcord.ui.button(label='Confirm', style=nextcord.ButtonStyle.green, row=1)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass
