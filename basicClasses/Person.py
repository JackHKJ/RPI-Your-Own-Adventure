# -*- encoding:utf-8 -*-
# Dependencies
from basicClasses.SkillTreeNode import SkillTreeNode
from basicClasses.SkillTree import SkillTree
from basicClasses.Request import Request

avail_list = ["Go to a concert in EMPAC", "Check the RPI website", "Tour around the campus", \
              "Talk to a RPI student", "Apply for RPI", "Introduce RPI to others"]  # list that is available
avail_list_student = ["Finished 4 4000-level courses", "Join 3 clubs", "Join the fraternity", \
                      "Work out at the RPI gym", "Join the sorosity", "Take the shuttel around the campus"]

class PersonBuilder():
    """
    This class is the builder for the person object
    """
    def __init__(self):
        self.person = Person()

    def set_name(self, name):
        """
        setter of the name
        :param name: name of the user
        """
        self.person.set_name(name)

    def set_location(self, location):
        """
        setter of the location
        :param location: location of the user
        """
        self.person.set_location(location)

    def set_gender(self, gender):
        """
        setter of the gender
        :param gender: gender of the user
        """
        self.person.set_gender(gender)

    def set_tel(self, tel):
        """
        setter of the tel
        :param tel: telephone of the user
        """
        self.person.set_tel(tel)

    def set_mail(self, mail):
        """
        setter of the mail
        :param mail: mail of the user
        """
        self.person.set_mail(mail)

    def set_request(self,user_type):
        """
        setter of the requests
        :param user_type: type of the user
        """
        if (user_type=="Guest"):
            for request in avail_list:
                self.person.add_avail_request(Request(request, [], ""))
        else:
            for request in avail_list_student:
                self.person.add_avail_request(Request(request, [], ""))

    def get_person(self):
        """
        getter of the Person object
        :return: person
        """
        return self.person

class Director():
    def __init__(self, builder):
        self.builder = builder

    def constructStudent(self,name):
        """
        Builder for a student type user
        :param name: name of the student
        :param skill_tree: skilltree for the student
        :param skills: skills to be added to the tree
        """
        self.builder.set_name(name)
        self.builder.set_gender("UNKNOWN")
        self.builder.set_location("TROY")
        self.builder.set_mail("UNKNOWN")
        self.builder.set_tel("UNKNOWN")
        self.builder.set_request("Student")

    def constructGuest(self,name):
        """
        Builder for a guest type user
        :param name: name of the guest
        """
        self.builder.set_name(name="Guest")
        self.builder.set_gender("UNKNOWN")
        self.builder.set_location("TROY")
        self.builder.set_mail("UNKNOWN")
        self.builder.set_tel("UNKNOWN")
        self.builder.set_request("Guest")

class Person(object):
    """
    This class is to represent a player in our game
    """

    def __init__(self):
        """
        The initializing function of the class
        """
        self.__name = None
        self.__location = None
        self.__gender = None
        self.__tel = None
        self.__mail = None
        self.__skills = set()
        self.__skillConnection = []
        self.__avail_request = []
        self.__accept_request = []

    def __str__(self):
        return "User [{}]".format(self.__name)

    def set_name(self,name):
        """
        setter of the name
        """
        self.__name = name

    def set_location(self,location):
        """
        setter of the location
        """
        self.__location = location

    def set_gender(self,gender):
        """
        setter of the gender
        """
        self.__gender = gender
    
    def set_mail(self,mail):
        """
        setter of the mail
        """
        self.__mail = mail

    def set_tel(self,tel):
        """
        setter of the telephone
        """
        self.__tel = tel

    def get_name(self):
        """
        Getter of the name
        :return: name
        """
        return self.__name

    def get_skills(self):
        """
        Getter of the skills
        :return: skills
        """
        return self.__skills

    def get_avail_request(self):
        """
        Getter of the list of available requests
        :return: list of available requests
        """
        return self.__avail_request

    def get_accept_request(self):
        """
        Getter of the list of accepted requests
        :return: list of accepted requests
        """
        return self.__accept_request

    def add_avail_request(self, request: Request):
        """
        Add available request to the person class
        :param request: the request to be added to the list of available requests
        :return: None
        """
        if request:
            self.__avail_request.append(request)

    def add_accept_request(self, request: Request):
        """
        Add accepted request to the person class
        :param request: the request to be added to the list of accepted requests
        :return: None
        """
        if request:
            self.__accept_request.append(request)

    def remove_avail_request(self, name):
        """
        remove an available request from the person class
        :param name: the name of the request to be removed from the list of available requests
        :return: the request removed or None if not found
        """
        for request in self.__avail_request:
            if request.get_name() == name:
                return self.__avail_request.pop(self.__avail_request.index(request))
        return None

    def remove_accept_request(self, name):
        """
        remove an accpeted request from the person class
        :param name: the name of the request to be removed from the list of accepted requests
        :return: the request removed or None if not found
        """
        for request in self.__accept_request:
            if request.get_name() == name:
                return self.__accept_request.pop(self.__accept_request.index(request))
        return None

    def check_finished(self, name):
        """
        check finished for an accpeted request from the person class
        :param name: the name of the request to be checked from the list of accepted requests
        :return None
        """
        for request in self.__accept_request:
            if request.get_name() == name:
                request.try_to_complete(self)

    def add_skill(self, main_tree: SkillTree, this_skill: SkillTreeNode):
        """
        Add skill to the person class
        :param main_tree: The main tree to look for connections
        :param this_skill: skill to be added
        :return: None
        """
        # If already contained, pass
        if this_skill in self.__skills:
            return
        self.__skills.add(this_skill)
        if this_skill.get_parent() is not None:
            for this_parent in this_skill.get_parent():
                if this_parent in self.__skills:
                    self.__skillConnection.append([str(this_parent), str(this_skill)])
        if this_skill.get_child() is not None:
            for this_child in this_skill.get_child():
                if this_child in self.__skills:
                    self.__skillConnection.append([str(this_child), str(this_skill)])

    def remove_skill(self, main_tree: SkillTree, this_skill: SkillTreeNode):
        """
        Remove a skill from the current representation
        :param main_tree: The main tree for usage
        :param this_skill: skill to be removed
        :return: None
        """
        if this_skill not in self.__skills:
            return
        updated_connection = []
        str_rep = str(this_skill)
        for connection in self.__skillConnection:
            if str_rep not in connection:
                updated_connection.append(connection)
        self.__skillConnection = updated_connection
        self.__skills.remove(this_skill)

    def add_skills_by_shortName(self, skill_tree: SkillTree, skills):
        """
        This function tries to add a list of skills by finding them in the main tree using shortNames
        :param skill_tree: the skill tree where the skills came from
        :param skills: a list of shortName of the skill to be added
        :return: None
        """
        for skill in skills:
            this_node = skill_tree.get_node_by_shortName(skill)
            if this_node is not None:
                self.add_skill(skill_tree, this_node)

    def get_selectable_courses(self, skillTree: SkillTree):
        """
        Get the selectable courses of a person
        :param skillTree: the skillTree to be utilized
        :return: list of SkillTreeNode that is selectable for the person
        """
        selectable_course = []
        for course in skillTree.get_node_set():
            if len(course.get_parent()) == 0 or (len(course.get_parent()) == 1 and course.get_parent()[0] == skillTree.get_root_node()):
                selectable_course.append(course)
                continue
            selectable = True
            for req in course.get_parent():
                if req not in self.__skills:
                    selectable = False
                    break
            if selectable and course not in self.__skills:
                selectable_course.append(course)
                continue
        return selectable_course

    def get_selectable_courses_filtered(self, skillTree: SkillTree, filter_str: str):
        """
        Get the selectable course with filter applied
        :param skillTree:the skillTree to be utilized
        :param filter_str:the filter to be applied
        :return:list of SkillTreeNode that is selectable for the person with filter applied
        """
        selectable_courses = self.get_selectable_courses(skillTree)
        if filter_str is None or filter_str == "":
            return selectable_courses
        filtered = []
        filter_str = filter_str.lower()
        for course in selectable_courses:
            if course.shortName.lower() == "root" or course.fullName.lower() == "root":
                continue
            if filter_str in (course.fullName.lower()) or filter_str in (course.shortName.lower()) or filter_str in \
                    course.ID:
                filtered.append(course)
        return filtered
