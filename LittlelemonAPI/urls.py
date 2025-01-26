from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [path('menu-items/', views.MenuItemsView.as_view(), name = 'menu-items'),
               path('category/', views.CategoriesView.as_view(), name = 'category'),
               path('menu-items/<int:id>', views.single_item),
               path('secret/', views.secret),
               path('manager-view/', views.manager_view, name='manager-view'),
               path('throttle-check/', views.throttle_check),
               path('throttle-check-auth/', views.throttle_check),
               path('api-token-auth/', obtain_auth_token),
               path('me/', views.me),
               path('groups/manager/users/', views.managers),
               path('manage-delivery-orders/', views.manage_delivery_orders),
               path('cart/menu-items/', views.cart_items),
               path('cart/orders/', views.customer_orders),
               path('delivery-crew/', views.delivery_crew),
               path('groups/delivery-crew/users/', views.DeliveryCrewViewSet.as_view(
                   {'get': 'list', 'post': 'create', 'delete': 'destroy'})
                    ),
               path('auth/', include('djoser.urls')),
               path('auth/', include('djoser.urls.authtoken')),
               ]
