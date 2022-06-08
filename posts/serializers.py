from rest_framework import serializers

from posts.models import Post, Vote


class PostSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    votes = serializers.SerializerMethodField(method_name='get_votes_post')

    class Meta:
        model = Post
        fields = ('id', 'title', 'url', 'created', 'poster', 'poster_id', 'votes')

    def get_votes_post(self, post):
        return Vote.objects.filter(post=post).count()


class VoteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='voter.id')

    class Meta:
        model = Vote
        fields = ('id',)
