from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_200_OK, HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Note
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404
from auth_app.models import CustomUser as User
from .serializers.note_serializer import NoteSerializer
from .utils import error_response, success_response
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.db.models import F, Case, When, Value, BooleanField
import json





class CreateNoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Set the permission classes
    authentication_classes = [JWTAuthentication] 
    
    
    def post(self, request):
        data = request.data
        note_id = data.get('noteId')  # Get the noteId from the request data
        
        # Check if noteId is present to determine if it's an update or create operation
        if note_id:
            try:
                note = Note.objects.get(id=note_id)
                note.title = data.get('title', note.title)
                content = data.get('content')
                if content:
                    note.content = json.dumps(content)  # Serialize JSON data to a string
                note.save()
                return Response({"message": "Note updated successfully"}, status=status.HTTP_200_OK)
            except Note.DoesNotExist:
                return Response({"message": "Note with the given ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            content = data.get('content', {})
            note = Note.objects.create(
                title=data.get('title', ''),
                content=json.dumps(content),  # Serialize JSON data to a string
                owner=request.user
            )
            return Response({"message": "Note created successfully"}, status=status.HTTP_201_CREATED)
    
    
    
    
class CustomPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
    

class NoteListView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Set the permission classes
    authentication_classes = [JWTAuthentication] 
    serializer_class = NoteSerializer

    def get(self, request):
        # Filter by the current user and not deleted
        queryset = Note.objects.filter(owner=request.user, is_deleted=False)

        # Annotate notes with a flag indicating whether they are pinned
        queryset = queryset.annotate(pinned=Case(
            When(pinned_at__isnull=False, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ))
        
        # Separate pinned and non-pinned notes
        pinned_notes = queryset.filter(pinned=True).order_by('-pinned_at')
        other_notes = queryset.filter(pinned=False).order_by('-updated_at')

        # Concatenate pinned notes and other notes
        queryset = list(pinned_notes) + list(other_notes)
        
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def delete(self, request):
        note_id = request.data.get('noteId')
        print(note_id)
        if note_id:
            try:
                note = Note.objects.get(id=note_id, owner=request.user)
                note.delete()
                return Response({"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            except Note.DoesNotExist:
                return Response({"message": "Note with the given ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Please provide a valid note ID"}, status=status.HTTP_400_BAD_REQUEST)
        


class ToggleNotePinStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Set the permission classes
    authentication_classes = [JWTAuthentication]  # Ensure user is authenticated
    
    def post(self, request):
        note_id = request.data.get('noteId')
        if note_id:
            # Get the note object or return 404 if not found
            note = get_object_or_404(Note, id=note_id, owner=request.user)
            # Toggle the pin status
            note.is_pinned = not note.is_pinned
            if note.is_pinned:
                # Set pinned_at timestamp if pinning the note
                note.pinned_at = timezone.now()
            else:
                # Clear pinned_at timestamp if unpinning the note
                note.pinned_at = None
            note.save()
            
            return success_response(message="Note pin status toggled successfully", status_code=status.HTTP_200_OK)
        else:
            return error_response(message="Please provide a valid note ID", status_code=status.HTTP_400_BAD_REQUEST)
            