def post_votes_increment(sender, instance, **kwargs):
    instance.post.increment_votes()


def post_votes_decrement(sender, instance, **kwargs):
    instance.post.decrement_votes()
