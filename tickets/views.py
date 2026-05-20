from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class   = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ('admin', 'agent'):
            return Ticket.objects.all().order_by('-created_at')
        return Ticket.objects.filter(created_by=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        user   = request.user
        # usuário comum só pode fechar o próprio chamado
        if user.role == 'user' and ticket.created_by != user:
            return Response({'detail': 'Sem permissão.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['patch'], url_path='assign')
    def assign(self, request, pk=None):
        ticket = self.get_object()
        user   = request.user
        if user.role not in ('admin', 'agent'):
            return Response({'detail': 'Sem permissão.'}, status=status.HTTP_403_FORBIDDEN)
        ticket.assigned_to = user
        ticket.status      = 'in_progress'
        ticket.save()
        return Response(TicketSerializer(ticket).data)

    @action(detail=True, methods=['patch'], url_path='status')
    def change_status(self, request, pk=None):
        ticket     = self.get_object()
        user       = request.user
        new_status = request.data.get('status')
        allowed    = ['open', 'in_progress', 'waiting', 'resolved', 'closed']
        if new_status not in allowed:
            return Response({'detail': 'Status inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        # usuário comum só pode fechar o próprio chamado
        if user.role == 'user':
            if ticket.created_by != user or new_status != 'closed':
                return Response({'detail': 'Sem permissão.'}, status=status.HTTP_403_FORBIDDEN)
        ticket.status = new_status
        ticket.save()
        return Response(TicketSerializer(ticket).data)