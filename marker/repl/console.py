import asyncio

import rich
from rich.console import Console as RichConsole
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn

from ..utils.console import ConsoleABC

class REPLConsole(ConsoleABC, RichConsole):
    def __init__(self):
        super().__init__()
    
    def error(self, *args, **kwargs):
        self.print(f'[-]', *args, style="red", **kwargs)

    def log(self, *args, **kwargs):
        self.print('[+]', *args, style="green", **kwargs)
    
    def get(self, prompt, **kwargs):
        return self.input(f'[yellow][?] {prompt}: ', **kwargs)

    def ask(self, prompt, default=False, **kwargs):
        y_or_n = "[Y]/n" if default else "y/[N]"
        answer = self.get(f'{prompt} {y_or_n}', **kwargs)
        if default == True:
            return "n" not in answer.lower()
        else:
            return "y" in answer.lower()
    
    def track(self, tasks, label="Processing"):
        progress = Progress(
            "[progress.description][yellow]{task.description} {task.fields[key]}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            console=self
        )
        with progress:
            task_bar = progress.add_task(label, total=len(tasks), key="")
            for idx, task in enumerate(tasks):
                progress.update(task_bar, completed=idx, key=task)
                yield task
            progress.update(task_bar, advance=1, key="finished")

    async def track_async(self, tasks, label="Processing"):
        with Progress(console=self) as progress:
            task_bar = progress.add_task("[yellow]"+label, total=len(tasks))
            results = []
            for task in asyncio.as_completed(tasks):
                try:
                    result = await task
                    results.append(result)
                except Exception as e:
                    self.error("Exception occured:", e)
                progress.update(task_bar, advance=1)
            return results