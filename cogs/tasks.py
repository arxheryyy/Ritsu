import discord
from discord.ext import commands, timers
from discord.ui import Button, View, Select
import sys

sys.path.append("/Users/archer/Documents/ritsu/modules")
from utils import *
import os

GUILD_ID = os.getenv("GUILD_ID")


class Tasks_cog(commands.Cog):
    def __init__(self, client):
        self.client: commands.bot = client

    @discord.slash_command(
        guild_ids=[GUILD_ID],
        description="Add task",
    )
    async def add_task(
        self,
        ctx,
        name: discord.Option(str, description="Name"),
        content: discord.Option(str, description="Content"),
    ):
        embed = discord.Embed(title="Please confirm", color=0x0000FF)
        embed.add_field(name=f"{name}", value=f"{content}", inline=False)
        confirm = Button(label="Confirm ✅", style=discord.ButtonStyle.green)
        cancel = Button(label="Cancel ❌", style=discord.ButtonStyle.red)

        async def confirm_callback(interaction):
            insert_task(name, content)
            embed = discord.Embed(title="Task added ✅")
            embed.add_field(name=f"{name}", value=f"{content}", inline=False)
            await interaction.response.edit_message(embed=embed, view=None)

        async def cancel_callback(interaction):
            embed = discord.Embed(title="Cancelled ✅")
            await interaction.response.edit_message(embed=embed, view=None)

        confirm.callback = confirm_callback
        cancel.callback = cancel_callback
        view = View(confirm, cancel)
        await ctx.respond(embed=embed, view=view, ephemeral=True)

    @discord.slash_command(
        guild_ids=[GUILD_ID],
        description="Get tasks",
    )
    async def tasks(self, ctx):
        embed = discord.Embed(title="Tasks", color=0x00FF00)
        all_tasks = get_tasks(done=False)
        if len(all_tasks) == 0:
            embed.add_field(
                name="No tasks found",
                value="Good job you finished your tasks.",
                inline=False,
            )
        else:
            for task in all_tasks:
                embed.add_field(
                    name=f"{task.id}. {task.name}",
                    value=f"{task.content}",
                    inline=False,
                )
        await ctx.respond(embed=embed, ephemeral=True)

    @discord.slash_command(
        guild_ids=[GUILD_ID],
        description="Finish tasks",
    )
    async def finish_task(self, ctx):
        select = Select(placeholder="Which task have you finished.")
        all_tasks = get_tasks(done=False)
        if len(all_tasks) == 0:
            embed = discord.Embed(title="No tasks found")
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            for task in all_tasks:
                select.add_option(label=f"{task.name}")
                select.callback = task.mark_done
            view = View(select)
            await ctx.respond(view=view, ephemeral=True)

    @discord.slash_command(
        guild_ids=[GUILD_ID],
        description="Get finished tasks",
    )
    async def finished_tasks(self, ctx):
        embed = discord.Embed(title="Finished tasks", color=0x00FF00)
        all_tasks = get_tasks(done=True)
        if len(all_tasks) == 0:
            embed.add_field(
                name="No tasks found", value="Get to work u lazy bitch.", inline=False
            )
        else:
            for task in all_tasks:
                embed.add_field(
                    name=f"{task.id}. {task.name}",
                    value=f"{task.content}",
                    inline=False,
                )
        await ctx.respond(embed=embed, ephemeral=True)

    @discord.slash_command(
        guild_ids=[GUILD_ID],
        description="Edit task",
    )
    async def edit_task(
        self,
        ctx,
        index: discord.Option(int, description="Index of task"),
        name: discord.Option(str, description="Name"),
        content: discord.Option(str, description="Content"),
    ):
        embed = discord.Embed(title="✅ Edited task", color=0x00FF00)
        edit_task(index, name, content)
        embed.add_field(name=f"{index}. {name}", value=f"{content}", inline=False)
        await ctx.respond(embed=embed, ephemeral=True)

    @discord.slash_command(
        guild_ids=[GUILD_ID],
        description="Reset DB",
    )
    async def reset_db(self, ctx):
        embed = discord.Embed(title="Please confirm", color=0xFF0000)
        embed.add_field(
            name="Reset DB", value="All tasks will be deleted", inline=False
        )
        confirm = Button(label="Confirm ✅", style=discord.ButtonStyle.green)
        cancel = Button(label="Cancel ❌", style=discord.ButtonStyle.red)

        async def confirm_callback(interaction):
            reset_db()
            embed = discord.Embed(title="DB has been reset ✅")
            await interaction.response.edit_message(embed=embed, view=None)

        async def cancel_callback(interaction):
            embed = discord.Embed(title="Cancelled ✅")
            await interaction.response.edit_message(embed=embed, view=None)

        confirm.callback = confirm_callback
        cancel.callback = cancel_callback
        view = View(confirm, cancel)
        await ctx.respond(embed=embed, view=view, ephemeral=True)


def setup(client):
    client.add_cog(Tasks_cog(client))
