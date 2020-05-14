# Python Modules

from abc import ABC, abstractmethod

# Application Modules

from app.classes.models.request import Status, SwapRequest, UserRequest
from app.classes.models.clockin import TemporarySwap
from app.classes.controllers.utils import timeslot_match, is_admin

# Flask Modules

class RequestControllerAbstract(ABC):
    """Contains common methods that all requestcontrollers should contain

    """

    @staticmethod  
    @abstractmethod
    def check_state(requestID):
        """Checks whether a request is in a resolved state

        Args: 
            requestID: associated request identifier

        Return:
            resolve: boolean indicating whether request resolvable or not.

        """
        pass

    @staticmethod
    @abstractmethod
    def resolve(requestID):
        """Makes changes to stored data reflecting the changes required by a
        request

        Args: 
            requestID: associated request identifier

        Return:
            resolved: boolean indicating whether operation was successful

        """
        pass
