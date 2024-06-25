from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from ..models.user import User
from ..serializers import UserSerializer
from utils.responses import success_response, error_response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message="Users retrieved successfully.",
            status_code=status.HTTP_200_OK,
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data,
            message="User retrieved successfully.",
            status_code=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
                data=request.data
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return success_response(
            data=serializer.data,
            message="User created successfully.",
            status_code=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return error_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
                data=request.data
            )
        self.perform_update(serializer)
        message = (
            "User partially updated successfully."
            if partial
            else "User updated successfully."
        )
        return success_response(
            data=serializer.data, message=message, status_code=status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_active:
            instance.is_active = False
            instance.save()
            return success_response(
                message="User archived successfully.",
                status_code=status.HTTP_204_NO_CONTENT,
            )
        else:
            return error_response(
                message="User is already archived.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
        permission_classes=[IsAuthenticated],
    )
    def restore(self, request, pk=None):
        instance = self.get_object()
        if not instance.is_active:
            instance.is_active = True
            instance.save()
            return success_response(
                message="User restored successfully.", status_code=status.HTTP_200_OK
            )
        else:
            return error_response(
                message="User is already active.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
