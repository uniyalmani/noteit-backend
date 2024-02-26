from django.urls import path
from .views import NoteListView,  CreateNoteView ,ToggleNotePinStatus, GenerateAndAccessSharedNoteAPIView, GetNoteByPublicIDAPIView

urlpatterns = [
    path('createnote/', CreateNoteView.as_view(), name="get new note"),
    path('togglepin/', ToggleNotePinStatus.as_view(), name="toggle pin status"),
    path('shared/<uuid:noteid>/', GenerateAndAccessSharedNoteAPIView.as_view(), name='generate-access-shared-note'),
     path('public/<uuid:public_id>/', GetNoteByPublicIDAPIView.as_view(), name='get-note-by-public-id'),
     path('', NoteListView.as_view() , name= "get notes"),
]