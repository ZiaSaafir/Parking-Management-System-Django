class AuthService:

    @staticmethod
    def is_admin(user):

        return (
            user.userprofile.role
            == "ADMIN"
        )

    @staticmethod
    def is_manager(user):

        return (
            user.userprofile.role
            == "MANAGER"
        )

    @staticmethod
    def is_operator(user):

        return (
            user.userprofile.role
            == "OPERATOR"
        )