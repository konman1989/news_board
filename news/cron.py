from posts.models import Vote


def reset_upvotes_count():
    Vote.objects.all().delete()
