# Description: Exception class for algoHub
class AlgoHubException(Exception):
    message = "AlgoHub error"
    status_code = 500

    def __init__(self, message, status_code=500):
        super(AlgoHubException, self).__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return self.message
