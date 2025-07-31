import asyncio
from desktop_notifier import DesktopNotifier

async def main():
    notifier = DesktopNotifier(app_name="My Awesome App")
    await notifier.send(
        title="Important Update",
        message="Your script has completed its task!",
    )

if __name__ == "__main__":
    asyncio.run(main())