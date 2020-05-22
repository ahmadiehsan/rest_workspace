import rules


# ===============
# defining rules
# =====
@rules.predicate
def is_article_author(user, article):
    return article.author == user


@rules.predicate
def is_vip_user(user):
    return user.is_authenticated and user.is_vip


is_member_of_editors = rules.is_group_member('editors')

# ===============
# combining rules
# =====
is_vip_or_editor = is_vip_user | is_member_of_editors
is_author_or_editor = is_article_author | is_member_of_editors
