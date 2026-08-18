import asyncio
import logging
import re
from typing import Callable, Awaitable

logger = logging.getLogger(__name__)

MessageHandler = Callable[[str, str], Awaitable[None]]

class MQTTRouter:
    def __init__(self):
        self._routes: list[tuple[re.Pattern, MessageHandler]] = []
        self._raw_topics: list[tuple[str, int]] = []

    def add_route(self, topic_pattern: str, handler: MessageHandler, qos: int = 1) -> None:
        regex_pattern = topic_pattern.replace("+", "[^/]+").replace("#", ".*")
        compiled_regex = re.compile(f"^{regex_pattern}$")
        self._routes.append((compiled_regex, handler))
        self._raw_topics.append((topic_pattern, qos))

    def get_subscription_topics(self) -> list[tuple[str, int]]:
        return self._raw_topics

    async def route(self, topic: str, payload: str) -> None:
        for pattern, handler in self._routes:
            if pattern.match(topic):
                await handler(topic, payload)
                return
        logger.warning(f"Dead letter: No handler registered for topic {topic}")


class MessageDispatcher:
    def __init__(self, router: MQTTRouter, queue: asyncio.Queue, max_workers: int):
        self.router = router
        self.queue = queue
        self.max_workers = max_workers
        self._workers: list[asyncio.Task] = []

    async def start(self) -> None:
        self._workers = [
            asyncio.create_task(self._worker_loop(i)) for i in range(self.max_workers)
        ]
        logger.info(f"Started {self.max_workers} background MQTT workers.")

    async def stop(self) -> None:
        await self.queue.join()
        for worker in self._workers:
            worker.cancel()
        await asyncio.gather(*self._workers, return_exceptions=True)

    async def _worker_loop(self, worker_id: int) -> None:
        while True:
            topic, payload = await self.queue.get()
            try:
                await self.router.route(topic, payload)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker {worker_id} unhandled error on {topic}: {str(e)}", exc_info=True)
            finally:
                self.queue.task_done()