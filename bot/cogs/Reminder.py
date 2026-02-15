import discord
from discord.ext import commands, tasks
from discord.ext.commands.context import Context
import re
import logging
import time
from datetime import datetime, timedelta
from ..db.database import ReminderDatabase

logger = logging.getLogger(__name__)


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = ReminderDatabase()
        self.check_reminders.start()
        logger.info("Reminder cog initialized successfully.")

    def cog_unload(self):
        self.check_reminders.cancel()

    def parse_time(self, time_str: str) -> int:
        """Parse time string like '30m', '2h', '1d' and return seconds."""
        match = re.match(r'^(\d+)([smhd])$', time_str.lower())
        if not match:
            return None
        
        value, unit = int(match.group(1)), match.group(2)
        
        multipliers = {
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 86400
        }
        
        return value * multipliers[unit]

    @tasks.loop(seconds=30)
    async def check_reminders(self):
        """Check for pending reminders every 30 seconds."""
        try:
            current_time = int(time.time())
            pending = self.db.get_pending_reminders(current_time)
            
            for reminder in pending:
                reminder_id, user_id, channel_id, guild_id, message, remind_at = reminder
                
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    
                    embed = discord.Embed(
                        title="⏰ Rappel",
                        description=message,
                        color=discord.Color.blue(),
                        timestamp=datetime.fromtimestamp(remind_at)
                    )
                    embed.set_footer(text="Rappel créé le")
                    
                    try:
                        await user.send(embed=embed)
                        logger.info(f"Reminder {reminder_id} sent to user {user_id}")
                    except discord.Forbidden:
                        try:
                            channel = self.bot.get_channel(int(channel_id))
                            if channel:
                                await channel.send(f"{user.mention}", embed=embed)
                                logger.info(f"Reminder {reminder_id} sent to channel {channel_id}")
                        except Exception as e:
                            logger.error(f"Failed to send reminder {reminder_id} to channel: {e}")
                    
                    self.db.mark_completed(reminder_id)
                    
                except Exception as e:
                    logger.error(f"Error processing reminder {reminder_id}: {e}")
                    self.db.mark_completed(reminder_id)
                    
        except Exception as e:
            logger.error(f"Error in check_reminders loop: {e}")

    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()

    @commands.command(name='remind')
    async def remind(self, ctx: Context, time_str: str, *, message: str):
        """Crée un rappel. Usage: $remind 30m Message ici"""
        seconds = self.parse_time(time_str)
        
        if seconds is None:
            await ctx.send("❌ Format de temps invalide. Utilisez: `30s`, `15m`, `2h`, `1d`")
            return
        
        if seconds < 10:
            await ctx.send("❌ Le délai minimum est de 10 secondes.")
            return
        
        if seconds > 86400 * 30:
            await ctx.send("❌ Le délai maximum est de 30 jours.")
            return
        
        current_time = int(time.time())
        remind_at = current_time + seconds
        
        user_id = str(ctx.author.id)
        channel_id = str(ctx.channel.id)
        guild_id = str(ctx.guild.id) if ctx.guild else None
        
        reminder_id = self.db.add_reminder(
            user_id=user_id,
            channel_id=channel_id,
            guild_id=guild_id,
            message=message,
            remind_at=remind_at,
            created_at=current_time
        )
        
        remind_datetime = datetime.fromtimestamp(remind_at)
        
        embed = discord.Embed(
            title="✅ Rappel créé",
            description=f"Je te rappellerai : **{message}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Dans", value=time_str, inline=True)
        embed.add_field(name="Le", value=remind_datetime.strftime("%d/%m/%Y à %H:%M"), inline=True)
        embed.set_footer(text=f"ID: {reminder_id}")
        
        await ctx.send(embed=embed)
        logger.info(f"Reminder {reminder_id} created for user {user_id}")

    @commands.command(name='reminders')
    async def list_reminders(self, ctx: Context):
        """Liste tous tes rappels actifs."""
        user_id = str(ctx.author.id)
        reminders = self.db.get_user_reminders(user_id)
        
        if not reminders:
            await ctx.send("📭 Vous n'avez aucun rappel actif.")
            return
        
        embed = discord.Embed(
            title="📋 Vos rappels actifs",
            color=discord.Color.blue()
        )
        
        for reminder_id, message, remind_at, created_at in reminders:
            remind_datetime = datetime.fromtimestamp(remind_at)
            time_left = remind_at - int(time.time())
            
            if time_left > 0:
                hours, remainder = divmod(time_left, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                if hours > 24:
                    days = hours // 24
                    time_left_str = f"{days}j {hours % 24}h"
                elif hours > 0:
                    time_left_str = f"{hours}h {minutes}m"
                else:
                    time_left_str = f"{minutes}m {seconds}s"
            else:
                time_left_str = "Bientôt"
            
            embed.add_field(
                name=f"#{reminder_id} - {remind_datetime.strftime('%d/%m %H:%M')}",
                value=f"{message}\n*Dans {time_left_str}*",
                inline=False
            )
        
        await ctx.send(embed=embed)

    @commands.command(name='remind_cancel')
    async def cancel_reminder(self, ctx: Context, reminder_id: int):
        """Annule un rappel par son ID. Usage: $remind_cancel 1"""
        user_id = str(ctx.author.id)
        
        if self.db.delete_reminder(reminder_id, user_id):
            await ctx.send(f"✅ Rappel #{reminder_id} annulé.")
            logger.info(f"Reminder {reminder_id} cancelled by user {user_id}")
        else:
            await ctx.send(f"❌ Rappel #{reminder_id} introuvable ou déjà complété.")


async def setup(bot):
    await bot.add_cog(Reminder(bot))
