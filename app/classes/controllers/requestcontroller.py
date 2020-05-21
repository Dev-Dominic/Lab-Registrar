# Python Modules

from abc import ABC, abstractmethod

# Application Modules

from app import db
from app.classes.models.request import Status, InfoType, SwapRequest, UserRequest
from app.classes.models.clockin import TemporarySwap
from app.classes.controllers.utils import timeslot_match, is_admin, find_user, generate_password

# Flask Modules

class RequestController(ABC):
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

class SwapRequestController(RequestController):
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
        """Checks whether a request is in a resolved state request

        Args:
            swapID: associated request identifier

        Return:
            is_resolvable: boolean indicating whether operation was successful

        """
        status = SwapRequestController.get_request(swapID).status
        is_resolvable = status == Status.CONFIRM
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
        if not SwapRequestController.check_state(swapID):
            return resolved

        request = SwapRequestController.get_request(swapID)

        # Checks whether request was resolved already

        if request.status in [Status.DENIED, Status.APPROVED]:
            return resolved

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

        if not swap_request.status in [Status.DENIED, Status.APPROVED]:
            swap_request.labtech_confirm_id = counterLabtechID
            swap_request.confirm_labtech_timeslot_id = counterTimeslotID
            swap_request.status = Status.CONFIRM

            db.session.commit()

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

        if not swap_request.status in [Status.DENIED, Status.APPROVED]:
            swap_request.admin_approve_id = adminID
            success = SwapRequestController.resolve(swapID)

            if success:
                swap_request.status = status
                db.session.commit()

        return success

class UserRequestController(RequestController):
    """Controls the various stages within a user request

    There are three stages:
        1. A user requests update to information
        2. Request approval by admin
        3. Resolved method is then called to make the necessary system

    """
    @staticmethod
    def get_request(userRequestID):
        """Queries SwapRequest instance associated with swapID

        Args:
            userRequestID: associated UserRequest identifier

        Return:
            user_request: UserRequest instance

        """
        user_request = UserRequest.query.filter_by(id=userRequestID).first()
        return user_request

    @staticmethod
    def check_state(userRequestID):
        """Checks whether a request is in a resolved request

        Args:
            swapID: associated request identifier

        Return:
            is_resolvable: boolean indicating whether operation was successful

        """
        status = UserRequestController.get_request(userRequestID).status
        is_resolvable =  status == Status.OPEN
        return is_resolvable

    @staticmethod
    def resolve(userRequestID):
        """Makes changes to stored data reflecting the changes required by a
        request

        Args:
            userRequestID: associated request identifier

        Return:
            resolved: boolean indicating whether operation was successful

        """
        resolved = False
        if UserRequestController.check_state(userRequestID):
            user_request = UserRequestController.get_request(userRequestID)

            # Checks whether a given request has already been resolved

            if user_request.status in [Status.DENIED, Status.APPROVED]:
                return False

            labtech = find_user(user_request.labtech_id)

            if user_request.infoType == InfoType.PASSWORD:
                labtech.password = generate_password(labtech.user_initials())
            else:
                # Using vars to get a dictionary of attributes
                # this allows for dynamically change instance attributes

                infoType = user_request.infoType.lower()
                vars(labtech)[infoType] = user_request.newInfo

            db.session.commit() # update labtech instance in database
            resolved = True
        return resolved

    @staticmethod
    def update(labtechID, infoType, newInfo):
        """Creates a new user/labtech request to update specific info

        Args:
            labtechID: labtech identifier
            infoType: infotype enum representing a user attribute

        Return:
            success: boolean indicating operation success

        """
        success = False
        labtech = find_user(labtechID)

        if labtech:
            user_request = UserRequest(labtechID, infoType, newInfo)
            db.session.add(user_request)

            db.session.commit()
            success = True

        return success

    @staticmethod
    def approve(adminID, userRequestID, status):
        """Allows an admin to approve or deny a given user request

        Args:
            adminID: user identifier that should represent an admin
            userRequestID: active user request identifier

        Return:
            success: boolean indicating operation success

        """
        success = False

        # Checks that adminID passed is valid and that
        # user_request actually exsits

        if is_admin(adminID):
            user_request = UserRequestController.get_request(userRequestID)
            if user_request:
                user_request.status = status
                success = UserRequestController.resolve(userRequestID)

        return success
