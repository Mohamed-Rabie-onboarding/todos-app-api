from bottle import Bottle


def patch_mount(app: Bottle):
    _mount = app.mount

    def mount(prefix: str, routes: Bottle, **options):
        plugins = app.plugins
        for plugin in plugins:
            routes.install(plugin)
        return _mount(prefix, routes, **options)

    app.mount = mount
