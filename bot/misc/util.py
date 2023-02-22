from bot.database.main import async_session


async def accept(request):
    async with async_session() as session:
        await session.execute(request)
        await session.commit()