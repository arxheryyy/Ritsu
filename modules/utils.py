import sqlite3
import discord


class Task:
    def __init__(self, id: int, name: str, content: str, done: bool):
        self.id = id
        self.name = name
        self.content = content
        self.done = done

    async def mark_done(self, interaction):
        db = sqlite3.connect("./main.sqlite", isolation_level=None)
        cursor = db.cursor()
        cursor.execute(
            f"""
            UPDATE tasks
            SET done = 1
            WHERE id = {self.id};
        """
        )
        embed = discord.Embed(title=f"✅ Success")
        embed.add_field(
            name=f"Marked as done", value=f"{self.id}. {self.name}", inline=False
        )
        await interaction.response.edit_message(embed=embed, view=None)


def insert_task(name: str, content: str):
    db = sqlite3.connect("./main.sqlite", isolation_level=None)
    cursor = db.cursor()
    cursor.execute(
        f"""
        INSERT INTO tasks (name, content)
        VALUES ('{name}', '{content}');
    """
    )


def reset_db():
    db = sqlite3.connect("./main.sqlite", isolation_level=None)
    cursor = db.cursor()
    cursor.execute("DROP TABLE tasks")
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS tasks
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            content TEXT,
            done INTEGER DEFAULT 0
        );
    """
    )


def get_tasks(done: bool):
    db = sqlite3.connect("./main.sqlite", isolation_level=None)
    cursor = db.cursor()
    if done:
        cursor.execute(
            f"""
            SELECT * FROM tasks WHERE done = 1;
        """
        )
        tasks = cursor.fetchall()
        all_tasks = []
        for task_item in tasks:
            id, name, content, done = task_item
            if done == 0:
                done = False
            elif done == 1:
                done = True
            item = Task(id, name, content, done)
            all_tasks.append(item)
    else:
        cursor.execute(
            f"""
            SELECT * FROM tasks WHERE done = 0;
        """
        )
        tasks = cursor.fetchall()
        all_tasks = []
        for task_item in tasks:
            id, name, content, done = task_item
            if done == 0:
                done = False
            elif done == 1:
                done = True
            item = Task(id, name, content, done)
            all_tasks.append(item)

    return all_tasks


def edit_task(index: int, name: str, content: str):
    db = sqlite3.connect("./main.sqlite", isolation_level=None)
    cursor = db.cursor()
    cursor.execute(
        f"""
        UPDATE 
            tasks
        SET name = '{name}',
            content = '{content}'
        WHERE 
            id = {index};
    """
    )
