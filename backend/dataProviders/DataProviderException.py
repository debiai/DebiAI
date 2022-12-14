# Description: Exception class for data providers
class DataProviderException(Exception):
    message = "Data provider error"
    status_code = 500

    def __init__(self, message, status_code=500):
        super(DataProviderException, self).__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return self.message