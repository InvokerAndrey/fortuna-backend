from core.views import BaseListView, BaseDetailView
from .models import Session
from .serializers import SessionSerializer, SessionDetailsSerializer


class SessionListView(BaseListView):
    model = Session
    serializer_class = SessionSerializer


class SessionDetailsView(BaseDetailView):
    model = Session
    serializer_class = SessionDetailsSerializer
