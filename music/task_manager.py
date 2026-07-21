import asyncio
import uuid

class MusicTaskManager:
    def __init__(self, generator):
        self.generator = generator
        self.tasks = {}
        self.queue = asyncio.Queue()

    async def worker(self):
        while True:
            task_id, prompt, filename = (
                await self.queue.get()
            )
            try:
                self.tasks[task_id] = {
                    "status":"running"
                }
                result = (
                    await asyncio.to_thread(
                        self.generator.generate,
                        prompt,
                        filename
                    )
                )
                self.tasks[task_id] = {
                    "status":"completed",
                    "file":result
                }
            except Exception as e:
                self.tasks[task_id]={
                    "status":"failed",
                    "error":str(e)
                }
            finally:
                self.queue.task_done()

    async def submit(
        self,
        prompt,
        filename
    ):
        task_id=str(
            uuid.uuid4()
        )
        self.tasks[task_id]={
            "status":"queued"
        }
        await self.queue.put(
            (
                task_id,
                prompt,
                filename
            )
        )
        return task_id

    def status(
        self,
        task_id
    ):
        return self.tasks.get(
            task_id,
            {
                "status":"not found"
            }
        )