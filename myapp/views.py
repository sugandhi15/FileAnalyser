from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import DocumentSerializer,UserSerializer
from .models import Document, User
from rest_framework.permissions import IsAuthenticated
from .jwt_helper import generate_jwt_token, decode_jwt_token
from django.contrib.auth.hashers import make_password, check_password

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            if User.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"}, status=400)
            request.data['password'] = make_password(request.data.get('password'))
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered successfully", "data": serializer.data, "token": generate_jwt_token(serializer.instance)})
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                token = generate_jwt_token(user)
                return Response({"message": "Login successful", "token": token})
            else:
                return Response({"error": "Invalid credentials"}, status=400)
            
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)



class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            print(f"Authorization Header: {auth_header}")

            if not auth_header:
                return Response({"error": "Authorization header missing"}, status=401)
            
            decoded_payload = decode_jwt_token(auth_header)
            print(f"Decoded Payload: {decoded_payload}")

            if 'error' in decoded_payload:
                return Response({"error": decoded_payload['error']}, status=401)

            user_id = decoded_payload.get('user_id')
            print(f"User ID: {user_id}")
            user = User.objects.get(id=user_id)
            print(f"User: {user}")
            # request.data['user'] = user.id
            # request.data['file'] = request.FILES.get('file')

            # if not request.data.get('file'):
            #     return Response({"error": "File is required"}, status=400)
            
            # if not user:
                # return Response({"error": "User not found"}, status=404)
            
            # data = request.data.copy()
            # data['user'] = user.id
            if not request.FILES.get('file'):
                return Response({"error": "File is required"}, status=400)
            
            data = request.data.copy()
            data['user'] = user_id
            data['file'] = request.FILES['file'] 
            print(f"Data to be serialized: {data}")

            serializer = DocumentSerializer(data=data)
            print(f"Serializer: {serializer}")
            print(f"Is serializer valid? {serializer.is_valid()}")

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "File uploaded successfully", "data": serializer.data})
            
            return Response(serializer.errors, status=400)
        
        except User.DoesNotExist as e:
            return Response({"error": "User not found", "details": str(e)}, status=404)
        except KeyError as e:
            return Response({"error": f"Missing key: {str(e)}"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        





class UserDocumentsView(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({"error": "Authorization header missing"}, status=401)
        
        try:
            decoded_payload = decode_jwt_token(auth_header)

            if 'error' in decoded_payload:
                return Response({"error": decoded_payload['error']}, status=401)

            user_id = decoded_payload.get('user_id')
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

            documents = Document.objects.filter(user=user)
            serializer = DocumentSerializer(documents, many=True)
            return Response({"documents": serializer.data}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)