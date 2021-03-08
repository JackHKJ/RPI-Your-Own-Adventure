# -*- encoding:utf-8 -*-
# Dependencies
# import SkillTreeNode
# import SkillTree
from enum import Enum, unique
from .Person import Person


@unique
class RequestStatusEnum(Enum):
    """
    The class for representing the status of the request
    """
    UNACCEPTABLE = "UNACCEPTABLE"
    ACCEPTABLE = "ACCEPTABLE"
    ACCEPTED = "ACCEPTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Request(object):
    """
    This class is used to define a "request", which should
    1. Check whether a request can be accepted (prerequisite)
    2. Hold the request and check for completion (Status check)
    3. Achievement after completion(None as default)
    """

    def __init__(self, request_name, prerequisite, achievement, complete_requirement, real_world_constrains=None):
        """
        The initializing function
        :param request_name: the name of the request
        :param prerequisite: prerequisite to be checked
        :param achievement: achievement to recieve
        """
        self.request_name = request_name
        self.prerequisite = prerequisite
        self.achievement = achievement
        self.real_world_constrains = real_world_constrains
        self.request_status = RequestStatusEnum.UNACCEPTABLE
        self.complete_requirement = complete_requirement
        # TODO: add more if necessary

    def get_name(self):
        """
        Getter of the name of the request
        :return: the name of the request
        """
        pass

    def get_achievement(self):
        """
        Check the status of the request to decide whether to return achievement
        :return: None if the status is not RequestStatusEnum.COMPLETED, return the achievement otherwise
        """

    def show_prerequisite(self):
        """
        Show the prerequisite of the request, this function is used to tell the user which prerequisite to get
        :return: a str representation of requirements
        """
        pass

    def check_prerequisite(self, person:Person):
        """
        Check whether the prerequisite is satisfied by the current state, modify the status if necessary
        :param person: the current state of the user
        :return: True if all prerequisite satisfied, False otherwise
        """
        pass

    def try_to_complete(self, person):
        """
        Try to complete the given request by examine the current state with the complete_requirements
        :param person: The current status of the requests
        :return: None
        """
        pass

    def __str__(self):
        """
        Getter of the str representation of hte request class, should at least show the name, status and other necessary
        information
        :return: the string representation of the request
        """
        pass
