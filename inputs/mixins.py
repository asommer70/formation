from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db.models import Q
from .models import Approval


class InputHolderMixin(object):
    def get_object(self, queryset=None):
        """
        Raise PermissionDenied if the current user didn't create the Input, or
        isn't the route_holder.
        """

        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg, None)
        queryset = queryset.filter(
            Q(pk=pk),
            Q(user=self.request.user) | Q(route_holder=self.request.user)
        )

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            try:
                # Allow users who have Approved an Input to view
                # it in the Archive.
                approvals = Approval.objects.filter(input_id=pk)
                obj = approvals.first().input
            except AttributeError:
                raise PermissionDenied

        return obj
