from .login import login_user
from .user import UserViewSet

# Note that all the views must be in plural
from .account import Accounts
from .group import Groups
from .forum_post import ForumPosts
from .task import Tasks
from .forum_commentary import ForumCommentaries
from .group_user import GroupUserSerializer, GroupUsers
