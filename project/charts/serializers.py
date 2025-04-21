from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueTogetherValidator


class NoticeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeInfo
        fields = [
            'notice_id',
            'company_id',
            'notice_job_category',
            'notice_location',
            'notice_career',
            'notice_title',
            'notice_position',
            'notice_main_work',
            'notice_qualification',
            'notice_preferred_qualification',
            'notice_welfare',
            'notice_category',
            'notice_end_date',
            'notice_tech_stack',
            'notice_url',
            'reg_dt',
            'mod_dt',]

class CompanyInfoSerializer(serializers.ModelSerializer):
    notices = NoticeInfoSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyInfo
        fields = [
            'company_id',
            'company_name',
            'company_tag',
            'company_salary',
            'company_location',
            'company_headcount',
            'company_revenue',
            'company_info',
            'reg_dt',
            'mod_dt',
            'notices',
            ]
# class QuestionSerializer(serializers.Serializer):
#    id = serializers.IntegerField(read_only=True)
#    question_text = serializers.CharField(max_length=200)
#    pub_date = serializers.DateTimeField(read_only=True)

#    def create(self, validated_data):
#        return Question.objects.create(**validated_data)

#    def update(self, instance, validated_data):
#        instance.question_text = validated_data.get('question_text', instance.question_text)
#        instance.save()
#        return instance

# class ChoiceSerializer(serializers.ModelSerializer):
#     #question = serializers.SlugRelatedField(slug_field='question_text', queryset=Question.objects.all())
#     class Meta:
#         model = Choice
#         fields = ['choice_text','votes']


# class QuestionSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#     choices = ChoiceSerializer(many=True, read_only=True)
#     class Meta:
#         model = Question
#         fields = ['id','question_text', 'pub_date','owner','choices']

# class UserSerializer(serializers.ModelSerializer):
#     questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
#     #questions = serializers.StringRelatedField(many=True, read_only=True)
#     #questions = serializers.SlugRelatedField(many=True, read_only=True, slug_field='pub_date')
#     #questions = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='question_detail')
#     class Meta:
#         model = User
#         fields = ['id','username','questions']

# class RegisterSerialzier(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#         return attrs
    
#     def create(self, validated_data):
#         user = User.objects.create_user(username=validated_data['username'])
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
    
#     class Meta:
#         model = User
#         fields = ['username','password','password2']
        

# class ChoiceSerializer(serializers.ModelSerializer):
#     votes_count = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Choice
#         fields = ['choice_text', 'votes_count']
        
#     def get_votes_count(self, obj):
#         return obj.votes_set.count()
    

# class VoteSerializer(serializers.ModelSerializer):    
#     voter = serializers.ReadOnlyField(source='voter.username')
        
#     class Meta:
#         model = Vote
#         fields = ['id', 'question', 'choice', 'voter']

# class VoteSerializer(serializers.ModelSerializer):
#     def validate(self, attrs):
#         if attrs['choice'].question.id != attrs['question'].id:
#             raise serializers.ValidationError("Question과 Choice가 조합이 맞지 않습니다.")
        
#         return attrs
    
#     class Meta:
#         model = Vote
#         fields = ['id', 'question', 'choice', 'voter']
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Vote.objects.all(),
#                 fields=['question', 'voter']
#             )
#         ]