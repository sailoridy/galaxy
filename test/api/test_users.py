from base import api

TEST_USER_EMAIL = "user_for_users_index_test@bx.psu.edu"


class UsersApiTestCase( api.ApiTestCase ):

    def test_index( self ):
        self._setup_user( TEST_USER_EMAIL )
        all_users_response = self._get( "users", admin=True )
        self._assert_status_code_is( all_users_response, 200 )
        all_users = all_users_response.json()
        # New user is in list
        assert len( [ u for u in all_users if u[ "email" ] == TEST_USER_EMAIL ] ) == 1
        # Request made from admin user, so should at least self and this
        # new user.
        assert len( all_users ) > 1

    def test_index_only_self_for_nonadmins( self ):
        self._setup_user( TEST_USER_EMAIL )
        with self._different_user():
            all_users_response = self._get( "users" )
            # Non admin users can only see themselves
            assert len( all_users_response.json() ) == 1

    def test_show( self ):
        user = self._setup_user( TEST_USER_EMAIL )
        with self._different_user( email=TEST_USER_EMAIL ):
            show_response = self.__show( user )
            self._assert_status_code_is( show_response, 200 )
            self.__assert_matches_user( user, show_response.json() )

    def __show( self, user ):
        return self._get( "users/%s" % ( user[ 'id' ] ) )

    def __assert_matches_user( self, userA, userB ):
        self._assert_has_keys( userB, "id", "username" )
        assert userA[ "id" ] == userB[ "id" ]
        assert userA[ "username" ] == userB[ "username" ]
