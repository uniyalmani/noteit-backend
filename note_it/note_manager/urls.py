from django.urls import path
from .views import NoteListView,  CreateNoteView ,ToggleNotePinStatus

urlpatterns = [
    path('createnote/', CreateNoteView.as_view(), name="get new note"),
    path('togglepin/', ToggleNotePinStatus.as_view(), name="toggle pin status"),
     path('', NoteListView.as_view() , name= "get notes"),
]