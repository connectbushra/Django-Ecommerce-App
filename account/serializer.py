# from rest_framework import serializers
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from django.contrib import auth
#
# class ResetPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField(min_length=2)
#     class Meta:
#         fields = ['email']

# class ChangePasswordSerializer(serializers.Serializer):
#     model :User
#
#     # old_password = serializers.CharField(required=True)
#     # new_password = serializers.CharField(required=True)
#     #
#     def save(self):
#         username = self.validated_data['username']
#         password = self.validated_data['password']
#         if username and password:
#             user = authenticate(username=username, password=password)
#             if user:
#                 if user.is_active:
#                     return user
#                 else:
#                     raise serializers.ValidationError({'user': 'user is not active'})
#             else:
#                 raise serializers.ValidationError({'user': 'please enter valid user credentails'})
#         else:
#              raise serializers.ValidationError({'error': 'username and password not to be blank'})
# class resetpasswordSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(max_length=100)
#     password = serializers.CharField(max_length=100)
#     class Meta:
#        model = User
#        fields = '__all__'
#
# def save(self):
#     username = self.validated_data['username']
#     password = self.validated_data['password']
#     # filtering out whethere username is existing or not, if your username is existing then if condition will allow your username
#     if User.objects.filter(username=username).exists():
#     # if your username is existing get the query of your specific username
#         user = User.objects.get(username=username)
#     # then set the new password for your username
#         user.set_password(password)
#         user.save()
#         return user
#     else:
#          raise serializers.ValidationError({'error': 'please enter valid crendentials'})
#
