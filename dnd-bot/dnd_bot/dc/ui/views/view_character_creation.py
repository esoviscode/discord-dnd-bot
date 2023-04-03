import nextcord

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.utils.message_holder import MessageHolder
from dnd_bot.logic.character_creation.chosen_attributes import ChosenAttributes
from dnd_bot.logic.character_creation.handler_character_creation import HandlerCharacterCreation
from dnd_bot.logic.prototype.classes.mage import Mage
from dnd_bot.logic.prototype.classes.ranger import Ranger
from dnd_bot.logic.prototype.classes.warrior import Warrior
from dnd_bot.logic.prototype.races.dwarf import Dwarf
from dnd_bot.logic.prototype.races.elf import Elf
from dnd_bot.logic.prototype.races.human import Human


class ViewCharacterCreationStart(nextcord.ui.View):
    """View shown at the beginning of character creation process"""

    def __init__(self, token):
        super().__init__(timeout=None)
        self.token = token

    @nextcord.ui.button(label='Next', style=nextcord.ButtonStyle.green, custom_id='start-next')
    async def next(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(ModalNameForm(interaction.user.id, self.token))


class ModalNameForm(nextcord.ui.Modal):
    """First form in character creation process"""
    def __init__(self, user_id, token):
        super().__init__("Name Form", timeout=None)
        self.user_id = user_id
        self.token = token

        self.name_textbox = nextcord.ui.TextInput(
            label="Name",
            placeholder="Enter your character name!",
            default_value=ChosenAttributes.chosen_attributes[user_id]['name'],
            custom_id='name-input'
        )

        self.backstory_textbox = nextcord.ui.TextInput(
            label="Background",
            placeholder="Tell something about your character's past!",
            default_value=ChosenAttributes.chosen_attributes[user_id]['backstory'],
            custom_id='background-input'
        )

        self.add_item(self.name_textbox)
        self.add_item(self.backstory_textbox)

    async def callback(self, interaction: nextcord.Interaction):
        """save user's choices and open alignment form"""
        ChosenAttributes.chosen_attributes[self.user_id]['name'] = self.name_textbox.value
        ChosenAttributes.chosen_attributes[self.user_id]['backstory'] = self.backstory_textbox.value
        await Messager.edit_last_user_message(user_id=self.user_id,
                                              embed=MessageTemplates.alignment_form_view_message_template(),
                                              view=ViewAlignmentForm(self.user_id, self.token))


class ViewAlignmentForm(nextcord.ui.View):
    """View with dropdowns for two axes of alignment"""
    def __init__(self, user_id, token):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.token = token
        self.lawfulness_axis_value = ChosenAttributes.chosen_attributes[self.user_id]['alignment'][0]
        self.goodness_axis_value = ChosenAttributes.chosen_attributes[self.user_id]['alignment'][1]

        lawfulness_option1 = nextcord.SelectOption(
            label="Lawful",
            description="You're honorable man and you like to follow the rules",
            emoji="📜",
            default=True if self.lawfulness_axis_value == 'Lawful' else False)

        lawfulness_option2 = nextcord.SelectOption(
            label="Neutral",
            description="You're not a rebel but rules are not sacred to you",
            emoji="⚖",
            default=True if self.lawfulness_axis_value == 'Neutral' else False)

        lawfulness_option3 = nextcord.SelectOption(
            label="Chaotic",
            description="You are a nonconforming, free man and you bow to no one",
            emoji="🤪",
            default=True if self.lawfulness_axis_value == 'Chaotic' else False)

        self.lawfulness_axis_dropdown = nextcord.ui.Select(
            placeholder="Law VS Chaos",
            options=[lawfulness_option1, lawfulness_option2, lawfulness_option3],
            row=0,
            custom_id='lawfulness-dropdown')

        goodness_option1 = nextcord.SelectOption(
            label="Good",
            description="Your altruism is beyond the scale",
            emoji="👼",
            default=True if self.goodness_axis_value == 'Good' else False)

        goodness_option2 = nextcord.SelectOption(
            label="Neutral",
            description="You don't kill the innocent neither you risk life for them",
            emoji="😐",
            default=True if self.goodness_axis_value == 'Neutral' else False)

        goodness_option3 = nextcord.SelectOption(
            label="Evil",
            description="You would sell your own mother with a smile on your face",
            emoji="😈",
            default=True if self.goodness_axis_value == 'Evil' else False)

        self.goodness_axis_dropdown = nextcord.ui.Select(
            placeholder="Good VS Evil",
            options=[goodness_option1, goodness_option2, goodness_option3],
            row=1,
            custom_id='goodness-dropdown')

        self.add_item(self.lawfulness_axis_dropdown)
        self.add_item(self.goodness_axis_dropdown)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red, row=2, custom_id='alignment-back')
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # save user's choices if they were made
        if self.lawfulness_axis_dropdown.values:
            ChosenAttributes.chosen_attributes[self.user_id]['alignment'][0] = self.lawfulness_axis_dropdown.values[0]

        if self.goodness_axis_dropdown.values:
            ChosenAttributes.chosen_attributes[self.user_id]['alignment'][1] = self.goodness_axis_dropdown.values[0]

        # delete error messages
        error_data = MessageHolder.read_last_error_data(self.user_id)
        if error_data is not None:
            MessageHolder.delete_last_error_data(self.user_id)
            await Messager.delete_message(error_data[0], error_data[1])

        await interaction.response.send_modal(ModalNameForm(self.user_id, self.token))

    @nextcord.ui.button(label='Next', style=nextcord.ButtonStyle.green, row=2, custom_id='alignment-next')
    async def next(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # save user's choices if they were made
        if self.lawfulness_axis_dropdown.values:
            ChosenAttributes.chosen_attributes[self.user_id]['alignment'][0] = self.lawfulness_axis_dropdown.values[0]

        if self.goodness_axis_dropdown.values:
            ChosenAttributes.chosen_attributes[self.user_id]['alignment'][1] = self.goodness_axis_dropdown.values[0]

        # check for previous error messages
        error_data = MessageHolder.read_last_error_data(self.user_id)

        # user hasn't made choice in at least one dropdown
        if (not self.lawfulness_axis_dropdown.values or not self.goodness_axis_dropdown.values) and \
            (not ChosenAttributes.chosen_attributes[self.user_id]['alignment'][0] or
             not ChosenAttributes.chosen_attributes[self.user_id]['alignment'][1]):

            if error_data is None:
                await Messager.send_dm_message(user_id=self.user_id, content="You must choose an alignment!", error=True)
            return

        # delete error messages
        if error_data is not None:
            MessageHolder.delete_last_error_data(self.user_id)
            await Messager.delete_message(error_data[0], error_data[1])

        await Messager.edit_last_user_message(user_id=self.user_id,
                                              embed=MessageTemplates.class_form_view_message_template(),
                                              view=ViewClassForm(self.user_id, self.token))


class ViewClassForm(nextcord.ui.View):
    """View with dropdown for selecting a class"""
    def __init__(self, user_id, token):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.token = token
        self.class_value = ChosenAttributes.chosen_attributes[self.user_id]['class']

        class_option1 = nextcord.SelectOption(
            label="Warrior",
            description="You like close encounters with your enemies.",
            emoji=Warrior.emoji(),
            default=True if self.class_value == 'Warrior' else False)

        class_option2 = nextcord.SelectOption(
            label="Mage",
            description="You're a magic freak.",
            emoji=Mage.emoji(),
            default=True if self.class_value == 'Mage' else False)

        class_option3 = nextcord.SelectOption(
            label="Ranger",
            description="A bow is your closest friend.",
            emoji=Ranger.emoji(),
            default=True if self.class_value == 'Ranger' else False)

        self.class_dropdown = nextcord.ui.Select(
            placeholder="Select a class.",
            options=[class_option1, class_option2, class_option3],
            row=0,
            custom_id='class-dropdown')

        self.add_item(self.class_dropdown)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red, row=1, custom_id='class-back')
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # save user's choices if they were made
        if self.class_dropdown.values:
            ChosenAttributes.chosen_attributes[self.user_id]['class'] = self.class_dropdown.values[0]

        # delete error messages
        error_data = MessageHolder.read_last_error_data(self.user_id)
        if error_data is not None:
            MessageHolder.delete_last_error_data(self.user_id)
            await Messager.delete_message(error_data[0], error_data[1])

        await Messager.edit_last_user_message(user_id=self.user_id,
                                              embed=MessageTemplates.alignment_form_view_message_template(),
                                              view=ViewAlignmentForm(self.user_id, self.token))

    @nextcord.ui.button(label='Next', style=nextcord.ButtonStyle.green, row=1, custom_id='class-next')
    async def next(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # save user's choices if they were made
        if self.class_dropdown.values:
            ChosenAttributes.chosen_attributes[self.user_id]['class'] = self.class_dropdown.values[0]

        error_data = MessageHolder.read_last_error_data(self.user_id)
        # user hasn't chosen any option
        if not self.class_dropdown.values and not ChosenAttributes.chosen_attributes[self.user_id]['class']:
            if error_data is None:
                await Messager.send_dm_message(user_id=self.user_id, content="You must choose a class!", error=True)
            return

        # delete error messages
        if error_data is not None:
            MessageHolder.delete_last_error_data(self.user_id)
            await Messager.delete_message(error_data[0], error_data[1])

        await Messager.edit_last_user_message(user_id=self.user_id,
                                              embed=MessageTemplates.race_form_view_message_template(),
                                              view=ViewRaceForm(self.user_id, self.token))


class ViewRaceForm(nextcord.ui.View):
    """View with dropdown for selecting a race"""
    def __init__(self, user_id, token):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.token = token
        self.race_value = ChosenAttributes.chosen_attributes[self.user_id]['race']

        race_option1 = nextcord.SelectOption(
            label="Human",
            description="Just an ordinary offspring of Adam.",
            emoji=Human.emoji(),
            default=True if self.race_value == 'Human' else False)

        race_option2 = nextcord.SelectOption(
            label="Elf",
            description="You have a lot of grace.",
            emoji=Elf.emoji(),
            default=True if self.race_value == 'Elf' else False)

        race_option3 = nextcord.SelectOption(
            label="Dwarf",
            description="You're a hard, tough worker.",
            emoji=Dwarf.emoji(),
            default=True if self.race_value == 'Dwarf' else False)

        self.race_dropdown = nextcord.ui.Select(
            placeholder="Select a race.",
            options=[race_option1, race_option2, race_option3],
            row=0,
            custom_id='race-dropdown')

        self.add_item(self.race_dropdown)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red, row=1, custom_id='race-back')
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # save user's choices if they were made
        if self.race_dropdown.values:
            ChosenAttributes.chosen_attributes[self.user_id]['race'] = self.race_dropdown.values[0]

        # delete error messages
        error_data = MessageHolder.read_last_error_data(self.user_id)
        if error_data is not None:
            MessageHolder.delete_last_error_data(self.user_id)
            await Messager.delete_message(error_data[0], error_data[1])

        await Messager.edit_last_user_message(user_id=self.user_id,
                                              embed=MessageTemplates.class_form_view_message_template(),
                                              view=ViewClassForm(self.user_id, self.token))

    @nextcord.ui.button(label='Confirm', style=nextcord.ButtonStyle.green, row=1, custom_id='race-confirm')
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # save user's choices if they were made
        if self.race_dropdown.values:
            ChosenAttributes.chosen_attributes[self.user_id]['race'] = self.race_dropdown.values[0]

        error_data = MessageHolder.read_last_error_data(self.user_id)
        # user hasn't chosen any option
        if not self.race_dropdown.values and not ChosenAttributes.chosen_attributes[self.user_id]['race']:
            if error_data is None:
                await Messager.send_dm_message(user_id=self.user_id, content="You must choose a race!", error=True)
            return

        await HandlerCharacterCreation.assign_attribute_values(self.user_id)

        # delete error messages
        if error_data is not None:
            MessageHolder.delete_last_error_data(self.user_id)
            await Messager.delete_message(error_data[0], error_data[1])

        await Messager.edit_last_user_message(user_id=self.user_id,
                                              embed=MessageTemplates.stats_retrospective_form_view_message_template(self.user_id),
                                              view=ViewStatsRetrospectiveForm(self.user_id, self.token))


class ViewStatsRetrospectiveForm(nextcord.ui.View):
    """View that allows to see stats and re-roll them once in a character creation process"""
    def __init__(self, user_id, token):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.token = token

    @nextcord.ui.button(label='Reroll', style=nextcord.ButtonStyle.red, row=1, custom_id='retrospective-reroll')
    async def reroll(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        button.disabled = True
        await HandlerCharacterCreation.assign_attribute_values(self.user_id)
        await Messager.edit_last_user_message(user_id=self.user_id,
                                              embed=MessageTemplates.stats_retrospective_form_view_message_template(
                                                  self.user_id),
                                              view=self)

    @nextcord.ui.button(label='Confirm', style=nextcord.ButtonStyle.green, row=1, custom_id='retrospective-confirm')
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        status, finished, error_message = \
            await HandlerCharacterCreation.handle_character_creation_finished(self.user_id, self.token)

        if status:
            if not finished:
                for component in self.children:
                    if isinstance(component, nextcord.ui.Button):
                        component.disabled = True
                await Messager.edit_last_user_message(user_id=self.user_id,
                                                      embed=MessageTemplates.stats_retrospective_form_view_message_template(
                                                          self.user_id),
                                                      view=self)

                await Messager.send_dm_message(user_id=self.user_id,
                                               content="You created your character! Now wait for other players to "
                                                       "finish!",
                                               error=True)
            else:
                # delete error messages
                error_data = MessageHolder.read_last_error_data(self.user_id)
                if error_data is not None:
                    MessageHolder.delete_last_error_data(self.user_id)
                    await Messager.delete_message(error_data[0], error_data[1])

        else:
            await interaction.response.send_message(error_message, ephemeral=True)
