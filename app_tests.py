#!flask/bin/python
import unittest
import flask_testing
from app import app, Addition, say_hello

# A set of basic unit tests to showcase simple test functionality
class BasicUnitTests(unittest.TestCase):
    # Tests must have 'test' in the function name or they are skipped
    @classmethod
    def this_gets_skipped(self):
        pass

    # functions that don't assert anything automatically pass
    # class method is used to evaluate non-instantiated stuff
    # if instantiated as a class method, you must explicitly provide the self argument to assertion functions
    @classmethod
    def test_should_auto_pass(self):
        pass

    # As an example, this test should fail
    def test_should_auto_fail(self):
        self.assertTrue(False,'This test was supposed to fail')

# A set of Flask-specific unit tests to showcase Flask related app functionality
class FlaskUnitTests(unittest.TestCase):
    # Creates an actual instantiation of the app, otherwise it wouldn't be running. This step can also include things
    # like loading databases and other stuff
    # since no assertion is made, we don't need this to be a test. If we use it in a try-block we can do an assertion
    # against the type error returned to verify its success
    @classmethod
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_type_error(self):
        self.assertRaises(ZeroDivisionError, Addition.div, 1,0)

    def test_Addition(self):
        # sends HTTP GET request to the application on the specified path
        result = dict(Addition().get())
        result = result['total']
        # check that the value returned by the function is correct
        self.assertTrue(result == 10,'test_Addition: Passed')

    def test_home_data(self):
        # sends HTTP GET request to the application on the specified path
        result = say_hello().get()
        # assert the response data
        self.assertEqual(result, "HELLO WORLD!")

    # this is where the app conducts a proper cleanup by removing database sessions, dropping tables, etc
    # this is not ran as a test because it doesn't include the word 'test' in the function name
    def tearDown(self):
        pass

    # Still trying to get this status code working, better to use a flask_testing TestCase instead I think
    # then you can call assert200() for example on a get() function for some resource

    #def test_home_status_code(self):
        ## sends HTTP GET request to the application on the specified path
        #result = app.get('/')
        ## assert the status code of the response
        #self.assertEqual(result.status_code, 200, '')


# A flask_testing set of unit tests (requires changing test runner I think)
#class FlaskTestingTests(flask_testing.TestCase):
    ## Tests must have 'test' in the function name or they are skipped
    #def test_200(self):
            ## sends HTTP GET request to the application on the specified path
            #result = say_hello().get()
            ## assert the response data
            #self.assert200(result,'')

# Without running unittest.main() or without using the conditional, it will break unit test detection
if __name__ == '__main__':
    unittest.main()
