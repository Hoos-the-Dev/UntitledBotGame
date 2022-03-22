from utils.utils import custom_id
import nextcord
import config

VIEW_NAME = "RoleView"


class RoleView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def handle_click(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        # get role from the role id
        role = interaction.guild.get_role(int(button.custom_id.split(":")[-1]))
        assert isinstance(role, nextcord.Role)
        # if member has the role, remove it
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            # send confirmation message
            await interaction.response.send_message(
                f"Your {button.label} role has been removed", ephemeral=True
            )
        # if the member does not have the role, add it
        else:
            await interaction.user.add_roles(role)
            # send confirmation message
            await interaction.response.send_message(
                f"You have been given the {button.label} role", ephemeral=True
            )

    @nextcord.ui.button(label="Updates", emoji="✔️", style=nextcord.ButtonStyle.primary, custom_id=custom_id(VIEW_NAME, config.SUBSCRIBER_ROLE_ID),)
  