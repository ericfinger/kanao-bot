import logging
from reaction_roles import *

logger = logging.getLogger(__name__)

"""

check if a message tries to role mention without using /ping
advise user if that's the case
Extensible for further message checks

"""
def get_on_message(bot):
    async def on_message(message):
        if message.author.bot:
            return
        if message.raw_role_mentions:
            if not message.author.guild_permissions.mention_everyone:
                logger.warning(f"User {message.author.name} tried to use raw role mentions without permissions in channel '{message.channel.name}'")
                await message.channel.send("Normal users need to use the /ping command to mention a role!", reference=message)
    return on_message


"""
log message edits
will not be called if the message isn't in the msg cache (anymore). 
the msg cache, by default is 5k, which i deem enough.
otherwise, on_raw_message_edit is recommended, or raising Client.max_messages

"""
def get_on_message_edit(bot):
    async def on_message_edit(before, after):
        if before.author.bot:
            return
        _editLogChannel = bot.get_channel(MESSAGE_EDIT_LOG)
        await _editLogChannel.send("```EDIT EVENT:\n\n" + "User: " + before.author.name + "\n\n" +
                            "Before: " + before.content + "\n\n" +
                            "After: " + after.content + "```")
    return on_message_edit


""" 

message delete event
same things as with on_message_edit apply

"""
def get_on_message_delete(bot):
    async def on_message_delete(message):
        _editLogChannel = bot.get_channel(MESSAGE_EDIT_LOG)
        await _editLogChannel.send("```MSG DELETE EVENT:\n\n" + "User: " + message.author.name + "\n\n" +
                            "Channel: " + message.channel.name + "\n"
                            "Message: " + message.content + "```")
    return on_message_delete


def get_on_raw_bulk_message_delete(bot):
    async def on_raw_bulk_message_delete(payload):
        _modLogChannel = bot.get_channel(MOD_LOG)
        _eventChannel = bot.get_channel(payload.channel_id)
        try:
            await _modLogChannel.send("```!! BULK DELETE EVENT !!" + "\n\n" + "Channel :" + _eventChannel.name + "\n\n"
                                     "Trying to get possibly cached messages: ```")
            for _msg in payload.cached_messages:
                await _modLogChannel.send("```" + _msg.author.name + ":\n" + _msg.content + "\n" + "```")

        except:
            await _modLogChannel.send("Failed getting any cached messages.")
    return on_raw_bulk_message_delete


def setup(bot, cmd_tree):
    bot.event(get_on_message(bot))
    bot.event(get_on_message_edit(bot))
    bot.event(get_on_message_delete(bot))
    bot.event(get_on_raw_bulk_message_delete(bot))

