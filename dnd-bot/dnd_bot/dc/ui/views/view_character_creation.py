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
            emoji=":man_judge:")

        lawfulness_option2 = nextcord.SelectOption(
            label="Neutral",
            description="You're not a rebel but not a completely trustworthy person either.",
            emoji=":scales:")

        lawfulness_option3 = nextcord.SelectOption(
            label="Chaotic",
            description="You are a free man and you bow to no one.",
            emoji=":zany_face:")

        self.lawfulness_axis_dropdown = nextcord.ui.Select(
            placeholder="Law VS Chaos",
            options=[lawfulness_option1, lawfulness_option2, lawfulness_option3])

        goodness_option1 = nextcord.SelectOption(
            label="Good",
            description="Your altruism is beyond the scale.",
            emoji=":angel:")

        goodness_option2 = nextcord.SelectOption(
            label="Neutral",
            description="You don't kill the innocent neither you risk your life for them.",
            emoji=":neutral_face:")

        goodness_option3 = nextcord.SelectOption(
            label="Evil",
            description="You would sell your own mother with a smile on your face.",
            emoji=":lying_face:")

        self.goodness_axis_dropdown = nextcord.ui.Select(
            placeholder="Good VS Evil",
            options=[goodness_option1, goodness_option2, goodness_option3])

    # TODO handle next and back buttons callbacks
    @nextcord.ui.button(label='Next', style=nextcord.ButtonStyle.green)
    async def next(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass
