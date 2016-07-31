from django.conf.urls import url, include
from api_views import token_view, database_view, table_view

urlpatterns = [
	url(r'^v1.0/token/$', token_view.TokenView.as_view(), name='token_view'),
	url(r'^v1.0/database/$', database_view.DatabaseView.as_view(), name='database_view'),
	url(r'^v1.0/table/$', table_view.TableView.as_view(), name='table_view'),
]
