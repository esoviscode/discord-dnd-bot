import nextcord


class MessageTemplates:

    @staticmethod
    def lobby_view_message_template(lobby_token):

        desc = "\nCampaign: 📜 Storm King's Thunder\n\n" \
               "Silentsky0 👑🔴\n\n" \
               "ziutek 🔵\n\n" \
               "cimek 🟤\n\n"

        embed = nextcord.Embed(title=f'Dungeons&Dragons 🐉 Lobby #{lobby_token}',
                               description=desc)

        # for player in players:
        #     pass

        embed.set_footer(text="The game will start when all the players are ready!")

        return embed
