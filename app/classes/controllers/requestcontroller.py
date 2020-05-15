# Python Modules

from abc import ABC, abstractmethod

# Application Modules

from app import db
from app.classes.models.request import Status, SwapRequest, UserRequest
from app.classes.models.clockin import TemporarySwap
from app.classes.controllers.utils import timeslot_match, is_admin

# Flask Modules

class RequestControllerAbstract(ABC):
    """Contains common methods that all requestcontrollers should contain

    """

    @staticmethod
    @abstractmethod
    def get_request(requestID): pass

    @staticmethod
    @abstractmethod
    def check_state(requestID):
        """Checks whether a request is in a resolved state

        Args:
            requestID: associated request identifier

        """
        pass

    @staticmethod
    @abstractmethod
    def resolve(requestID):
        """Makes changes to stored data reflecting the changes required by a
        request

        Args:
            requestID: associated request identifier

        """
        pass

# TODO redudancy in check_state and resolve
# Making query to SwapRequest twice
# Need for exception handling in each method

class SwapRequestController(RequestControllerAbstract):
    """Controls the various stages within a timeslot swap request

    There are four stages:
        1. A lab tech requests a temporary timeslot swap
        2. Another lab tech counters this request with a timeslot they are
        associated with
        3. An admin user then approves this swap, were it is then SwapRequestController.resolved
        4. Resolved method is then called to make the necessary system
        adjustments to facilitate this swap.

    """

    @staticmethod
    def get_request(swapID):
        """Queries SwapRequest instance associated with swapID

        Args:
            swapID: associated SwapRequest identifier

        Return:
            swap_request: SwapRequest instance

        """
        swap_request = SwapRequest.query.filter_by(id=swapID).first()
        return swap_request

    @staticmethod
    def check_state(swapID):
        """Checks whether a request is in a reo
        request

        Args:
            swapID: associated request identifier

        Return:
            is_resolvable: boolean indicating whether operation was successful

        """
        is_resolvable = SwapRequestController.get_request(swapID).status == Status.APPROVED
        return is_resolvable

    @staticmethod
    def resolve(swapID):
        """Makes changes to stored data reflecting the changes required by a
        request

        Args:
            swapID: associated request identifier

        Return:
            resolved: boolean indicating if the operation was successful

        """
        resolved = False
        if SwapRequestController.check_state(swapID):
            return resolved

        request = SwapRequestController.get_request(swapID)

        # Adding two entries into TemporarySwap reflecting swap of timeslots

        temp_swap_one = TemporarySwap(request.labtech_request_id,
                                      request.confirm_labtech_timeslot_id)
        temp_swap_two = TemporarySwap(request.labtech_confirm_id,
                                      request.request_labtech_timeslot_id)

        db.session.add(temp_swap_one)
        db.session.add(temp_swap_two)
        db.session.commit()

        resolved = True
        return resolved

    @staticmethod
    def request_swap(labtechID, timeslotID):
        """Creates SwapRequest indicating a labtech wants a temporary swap of
        timeslots.

        Args:
            labtechID: labtech identifier
            timeslotID: timeslot identifier that should correspond with
            labtechID

        Return:
            success: boolean indicating swap request was recorded

        """
        success = False
        if not timeslot_match(labtechID, timeslotID):
            return success

        swap_request = SwapRequest(labtechID, timeslotID)

        db.session.add(swap_request)
        db.session.commit()

        success = True
        return success

    @staticmethod
    def accept_swap(counterLabtechID, counterTimeslotID, swapID):
        """Adding counterLabTech offer to a given swap request

        Args:
            counterTimeslotID: labtech accepting possible swap

        Return:
            success: boolean indicating swap request was recorded

        """
        success = False
        if not timeslot_match(counterLabtechID, counterTimeslotID):
            return success

        # Retrieving SwapRequest and updating request
        swap_request = SwapRequestController.get_request(swapID)

        swap_request.labtech_confirm_id = counterLabtechID
        swap_request.confirm_labtech_timeslot_id = counterTimeslotID
        swap_request.status = Status.CONFIRM

        db.commit.session()

        success = True
        return success


    @staticmethod
    def approve_swap(adminID, status, swapID):
        """Admin approval or denial of a swap request

        Args:
            adminID: user admin identifier
            status: updated Status code for the request
            swapID: related swap that should be updated

        Return:
            success: boolean indicating swap request was approved or denied

        """
        success = False
        if not is_admin(adminID):
            return success

        swap_request = SwapRequestController.get_request(swapID)

        # Updates to swap request instance

        swap_request.admin_approve_id = adminID
        swap_request.status = status

        success = SwapRequestController.resolve(swapID)
        return success
