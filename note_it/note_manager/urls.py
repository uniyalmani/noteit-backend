from django.urls import path
from .views import NoteListView,  CreateNoteView 

urlpatterns = [
    path('createnote/', CreateNoteView.as_view(), name="get new note"),
    path('', NoteListView.as_view() , name= "get notes")
]