from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from pos.serializers import *
from pos.models import *

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def receipts_list(request, format=None):
    """ Receipts list associated with auth user."""
    if request.method == 'GET':
        # Retrieve all receipts that owned by user.
        try:
            receipts = Receipt.objects.filter(user=request.user)
            receipts_serialized = ReceiptSerializer(receipts, many = True)
            return Response(receipts_serialized.data)
        except:
            request.user.receipts = []
            return Response([])

    if request.method == 'POST':
        # Insert new receipt.
        receipt_instance = ReceiptPOSTSerializer(data=request.data)
        if receipt_instance.is_valid():
            receipt_instance.save()
            return Response(receipt_instance.data, status=status.HTTP_201_CREATED)
        return Response(receipt_instance.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def receipt_instance(request, receipt_id, format=None):
    try:
        receipt = Receipt.objects.get(pk=receipt_id)
    except Receipt.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReceiptSerializer(receipt)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReceiptPOSTSerializer(receipt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        receipt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def items_list(request, receipt_id=0, format=None):
    """ All items available or some related to receipt_id."""
    if request.method == 'GET':
        # Retrieve all receipts that owned by user.
        if receipt_id:
            items = Item.objects.filter(receipt=receipt_id)
        else:
            items = Item.objects.all()
        items_serialized = ItemSerializer(items, many = True)
        return Response(items_serialized.data)


    if request.method == 'POST':
        # Insert new item.
        item_instance = ItemPOSTSerializer(data=request.data)
        if item_instance.is_valid():
            item_instance.save()
            return Response(item_instance.data, status=status.HTTP_201_CREATED)
        return Response(item_instance.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def item_instance(request, item_id, format=None):
    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ItemPOSTSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        receipt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def topic_instance(request, pk, format = None):
    """
    Returns a topic instance if GET
    """

    # Validates that user has an access on this instance. 
    if not restrict_access(request, pk):
        return Response(status = status.HTTP_400_BAD_REQUEST)

    try:
        topic_instance = Topic.objects.get(pk = pk)
    except Topic.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        topics_serialized = TopicSerializer(topic_instance)
        return Response(topics_serialized.data)

@api_view(['GET'])
def topic_faculty(request, fac_id, format = None):
    """
    Returns all topics associated with specific faculty as {'dep':{topic1, topic2, ...etc}, 'dep2':{topic1, topic2, ...ect}, ...etc}
    """

    # Check the existence of faculty id.
    try:
        faculty = Faculty.objects.get(pk = fac_id)
    except Faculty.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    departments = faculty.departments.all()

    if departments:
        # Buliding the result dictionary.
        # {'dep':{topic1, topic2, ...etc}, 'dep2':{topic1, topic2, ...ect}, ...etc}
        departments_topics = {}
        for dep in departments:
            departments_topics[dep.name] = Topic.objects.filter(department = dep).values('id', 'name')

        topics_serialized = FacultyTopicsSerializer(faculty, context = {'topics': departments_topics})
        return Response(topics_serialized.data)

    return Response(status = status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def user_topics(request, format = None):
    """
    Returns list of user's topics if get, Update user's selection if post.
    """

    if request.method == 'GET':
        topics              = request.user.profile.topics
        topics_serialized   = TopicSerializer(topics, many = True)
        return Response(topics_serialized.data)

    if request.method == 'POST':
        user_choices = request.POST.getlist('chosen_list[]', None)
        if not user_choices or not within_user_domain(request.usser, user_choices):
            return Response(status = status.HTTP_400_BAD_REQUEST)

        if(UserTopics.update_topics(request, user_topics)):
            return Response(status = status.HTTP_201_CREATED)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def materials_list(request, topic_id, format = None):
    """
    Return a list of materials related to specific topic using GET
    """

    # Validates that user has an access on this instance. 
    if not restrict_access(request, topic_id):
        return Response(status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        try:
            topic_instance = Topic.objects.get(pk = topic_id)
        except Topic.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        materials               = Material.objects.filter(topic_id = topic_id).all()
        materials_serialized    = MaterialSerializer(materials, many = True)
        return Response(materials_serialized.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def tasks_list(request, format = None):
    """
    Return a list of tasks whose deadlines are to be met.
    """
    if request.method == 'GET':
        tasks               = Task.get_closest_tasks(request)
        tasks_serialized    = TasksSerializer(tasks, many = True)
        return Response(tasks_serialized.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def exams_list(request, topic_id, format = None):
    """List of topic's exams if GET."""

    # Validates that user has an access on this instance. 
    if not restrict_access(request, topic_id):
        return Response(status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        try:
            topic_instance = Topic.objects.get(pk = topic_id)
        except Topic.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        exams = topic_instance.exams.all()
        exams_serialized = ExamSerializer(exams, many=True)
        return Response(exams_serialized.data)

@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
def query_dep_table(request, format = None):
    """Query dep table with paramaters via POST. Returns query parameters via GET."""

    if request.method == 'POST':
        topics = request.POST.getlist('topics', None)
        professors = request.POST.getlist('professors', None)
        periods = request.POST.getlist('periods', None)
        days = request.POST.getlist('days', None)
        table = DepartmentTable(request.user)
        
        # results[0] -> table, results[1] -> choices
        results = table.query_table(request.user, topics, professors, periods, days)
        request.session['choices'] = results[1]

        if(results[0]):
            json_table = json.dumps(results[0])
            return Response(json_table)
        else:
            return Response(status = status.HTTP_404_NOT_FOUND)

    elif request.method == 'GET':
        try:
            # Grapping user department table.
            json_table = {}
            if request.user.profile:
                dep_table = DepartmentTable(request.user)
                result = DepartmentTableSerializer(dep_table)
            return Response(result.data)
        except ObjectDoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)