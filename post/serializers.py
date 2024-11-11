from rest_framework import serializers
from .models import Post, Reaction, Report, Block


class PostSerializer(serializers.ModelSerializer):
    user_reaction = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 
                  'support_count', 'empathy_count', 'congratulations_count', 
                  'luck_count', 'user_reaction']

    def get_user_reaction(self, obj):
        user = self.context['request'].user
        # 사용자가 현재 게시물에 남긴 공감 유형을 가져 온다
        reaction = Reaction.objects.filter(user=user, post=obj).first()
        return reaction.reaction_type if reaction else None


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id', 'user', 'post', 'reaction_type']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'user', 'post']


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['id', 'user', 'post']
