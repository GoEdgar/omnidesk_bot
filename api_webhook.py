from aiohttp import web

routes = web.RouteTableDef()

@routes.post('/change_status')
async def change_status(request):
    print(request, type(request))
    return 

app = web.Application()
app.add_routes(routes)
web.run_app(app)