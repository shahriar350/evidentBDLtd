from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from search_app.models import UserInput
from search_app.serializers import InputSaveSerializer, InputSearchSerializer


# Create your views here.
class InputSave(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InputSaveSerializer


class InputSearch(RetrieveAPIView):
    serializer_class = InputSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        data = UserInput.objects.filter(user=self.request.user, input=self.kwargs.get("input"))
        if data.exists():
            return data.first()
        else:
            raise UserInput.DoesNotExist


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_whole_data(request):
    data = {
        "status": "success",
        'user_id': request.user.id,
        'payloads': []
    }
    groups = UserInput.objects.filter(user=request.user).values_list("date_created", flat=True).distinct().all()

    for i in groups:
        nums = ",".join(str(d.input) for d in UserInput.objects.filter(date_created=i).all())
        val = {'timestamp': i.strftime('%Y-%m-%d %H:%M'), "input_values": nums}
        data['payloads'].append(val)
    return Response(data=data, status=200)
