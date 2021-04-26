# -*- encoding:utf-8 -*-
# Dependencies
# import SkillTreeNode
# import SkillTree
from enum import Enum, unique
# from .Person import Person
from basicClasses.Node import Node


@unique
class RequestStatus(Enum):
    """
    The class for representing the status of the request
    """
    UNACCEPTABLE = "UNACCEPTABLE"
    ACCEPTABLE = "ACCEPTABLE"
    ACCEPTED = "ACCEPTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Request(Node):
    """
    This class is used to define a "request", which should
    1. Check whether a request can be accepted (prerequisite)
    2. Hold the request and check for completion (Status check)
    3. Achievement after completion(None as default)
    """

    def __init__(self, ID, prerequisite, achievement, complete_requirement=None, real_world_constrains=None):
        """
        The initializing function
        :param ID: the identification string of the request
        :param prerequisite: prerequisite to be checked
        :param achievement: achievement to receive
        """
        super().__init__(ID)
        self.__request_name = ID
        self.__prerequisite = prerequisite
        self.__achievement = achievement
        self.__real_world_constrains = real_world_constrains
        self.__request_status = RequestStatus.UNACCEPTABLE
        self.__complete_requirement = complete_requirement

    def get_name(self):
        """
        Getter of the name of the request
        :return: the name of the request
        """
        return self.__request_name

    def get_achievement(self):
        """
        Check the status of the request to decide whether to return achievement
        :return: None if the status is not RequestStatusEnum.COMPLETED, return the achievement otherwise
        """
        if self.__request_status == RequestStatus.COMPLETED:
            return self.__achievement
        else:
            return None

    def show_prerequisite(self):
        """
        Show the prerequisite of the request, this function is used to tell the user which prerequisite to get
        :return: a str representation of requirements
        """
        prerequisite_string = ""
        for prerequisite_list in self.__prerequisite:
            prerequisite_string += "("
            for i in range(len(prerequisite_list)):
                prerequisite_string += " " + prerequisite_list[i] + " "
                if i != len(prerequisite_list) - 1:
                    prerequisite_string += "or"
            prerequisite_string += ")\n"
        return prerequisite_string

    def check_prerequisite(self, person):
        """
        Check whether the prerequisite is satisfied by the current state, modify the status if necessary
        :param person: the current state of the user
        :return: True if all prerequisite satisfied, False otherwise
        """
        return self.__check_prerequisites(self.__prerequisite, person.get_skills())

    def try_to_complete(self, person):
        """
        Try to complete the given request by examine the current state with the complete_requirements
        :param person: The current status of the requests
        :return: None
        """
        """
        For now, assuming that there is no complete_requirements
        """
        self.__request_status = RequestStatus.COMPLETED

    def __str__(self):
        """
        Getter of the str representation of the request class, should at least show the name, status and other necessary
        information
        :return: the string representation of the request
        """
        if self.__request_status == RequestStatus.COMPLETED:
            return "FINISHED: {}".format(self.__request_name)
        return self.__request_name

    def __check_prerequisites(self, pl, skills, mode=all):
        """
        Private method to check whether the prerequisites have been satisfied
        recursively
        :param pl: list or sublist of prerequisites
        :param skills: an iterable containing the already acquired skills
        :return: True if the prerequisites are satisfied, False otherwise
        """
        if type(pl) != list:
            for s in skills:
                if s.shortName == pl:
                    return True
            return False

        m = any
        if mode == any:
            m = all
        return mode([self.__check_prerequisites(x, skills, m) for x in pl])
