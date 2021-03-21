import rich
import asyncio
from time import sleep
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn
from rich.console import Console

class MyConsole(Console):
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
            task_bar = progress.add_task(label, total=len(tasks), key=tasks[0])
            for task in tasks:
                yield task
                progress.update(task_bar, advance=1, key=task)

    async def track_async(self, tasks, label="Processing"):
        with Progress(console=self) as progress:
            task_bar = progress.add_task("[yellow]"+label, total=len(tasks))
            results = []
            for task in asyncio.as_completed(tasks):
                try:
                    result = await task
                    results.append(result)
                except Exception as e:
                    console.error("Exception occured:", e)
                progress.update(task_bar, advance=1)
            return results
        
console = MyConsole()







if __name__ == "__main__":
    lst = list(range(100))
    for i in progress_iter(lst, "Counting"):
        if (i % 10) == 0:
            print(i)
        sleep(0.02)
    pass

    import aiohttp

    URL = 'https://httpbin.org/uuid'

    async def fetch(session, url):
        async with session.get(url) as response:
            json_response = await response.json()
            # print(json_response['uuid'])

    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = [fetch(session, URL) for _ in range(1000)]
            await progress_futures(tasks, "Getting URLs")

    # asyncio.run(main())

    console.log("This is a regular log", "oh no")
    console.error("Something went wrong big time")