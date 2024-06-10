# Description: Exception class for data providers
class DataProviderException(Exception):
    message = "Data provider error"
    status_code = 500

    def __init__(self, message=None, status_code=None):
        super(DataProviderException, self).__init__(message)

        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code

    def __str__(self):
        return self.message
