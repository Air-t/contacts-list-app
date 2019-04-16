from django.urls import path
from django.conf import settings

from django.conf.urls.static import static
from contacts.views import ContactList, PersonView, AddPersonAddress, ModifyPersonAddress, AddPersonEmail, \
    ModifyPersonEmail, AddPersonPhone, ModifyPersonPhone, GroupsView, AddGroupView, ModifyGroupView, AddToGroupView, \
    RemoveFromGroupView, GroupView, SearchGroupView

app_name = 'contacts'

urlpatterns = [
                  path('', ContactList.as_view(), name='contact_list'),
                  path('contact/<int:id>/', PersonView.as_view(), name='contact'),
                  path('contact/<int:id>/new-address/', AddPersonAddress.as_view(), name='add-address'),
                  path('contact/<int:id>/modify-address/<int:address_id>/', ModifyPersonAddress.as_view(),
                       name='modify-address'),
                  path('contact/<int:id>/new-email/', AddPersonEmail.as_view(), name='add-email'),
                  path('contact/<int:id>/modify-email/<int:email_id>/', ModifyPersonEmail.as_view(),
                       name='modify-email'),
                  path('contact/<int:id>/new-phone/', AddPersonPhone.as_view(), name='add-phone'),
                  path('contact/<int:id>/modify-phone/<int:phone_id>/', ModifyPersonPhone.as_view(),
                       name='modify-phone'),

                  path('groups/', GroupsView.as_view(), name='groups'),
                  path('groups/add-group/', AddGroupView.as_view(), name='add-group'),
                  path('groups/add-to-group/<int:id>/', AddToGroupView.as_view(), name='add-to-group'),
                  path('groups/remove-from-group/', RemoveFromGroupView.as_view(), name='remove-from-group'),
                  path('groups/modify-group/<int:group_id>/', ModifyGroupView.as_view(), name='modify-group'),
                  path('groups/group/<int:id>/', GroupView.as_view(), name='group'),
                  path('groups/group/<int:id>/search/', SearchGroupView.as_view(), name='search'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
