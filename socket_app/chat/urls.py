from chat import views

routes = (
    dict(method='GET', path='/', handler=views.index, name='index'),
)