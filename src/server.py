from aiohttp import web

from wechaty import (
    Contact,
    Room,
    FileBox,
    Message,
    Wechaty,
    Friendship)

routes = web.RouteTableDef()

context = dict()

def bot_view_wrapper(view_func):
    """
    A decorator which automatically add bot and path match as params into the view function.
    Extends the pure aiohttp way.
    :param view_func:
    :return:
    """

    async def _view(request: web.Request):
        return await view_func(
            request,
            bot=context.get('bot')
        )

    return _view


@routes.post(r'/room/send_message')
@bot_view_wrapper
async def view(request: web.Request, bot: Wechaty):
    request_json = await request.json()
    msg = request_json.get('msg')
    urls = request_json.get('urls')

    room: Room = await bot.Room.find(request_json.get('room'))
    if not room:
        print('Bot ' + 'there is no room topic ' + request_json.get('room') + '(yet)')
        return

    if msg:
        await room.say(msg)

    if urls:
        for url in urls:
            image_file = FileBox.from_url(url,name='image.jpg')
            await room.say(image_file)

    return web.json_response(data=dict(msg='Success'))

async def puppetware_start_server(bot, host='0.0.0.0', port=8082):
    context['bot'] = bot

    app = web.Application()
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, host, port)
    await site.start()
