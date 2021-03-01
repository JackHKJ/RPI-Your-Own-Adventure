# -*- encoding:utf-8 -*-
# Dependencies

class SkillTreeNode():
    """
    This is the class designed for represent a single course in the full skill tree
    """

    def __init__(self, ID=None, fullName="", shortName="", skillType="", additionalInfo="", passReq=None,
                 is_abstract=False):
        """
        Initializing the representation
        :param ID: CRN/Other unique identification number, used for verifying equal
        :param fullName: Name of the Skill
        :param shortName: Short Name for Hash/Search
        :param skillType: Type of the skill
        :param additionalInfo: Other important information about this course
        :param passReq: Some requirement to pass the course
        :param is_abstract: Whether this node is abstract(used for classification purpose)
        """
        if ID is None:
            raise Exception("Error, ID must be entered")
        self.ID = ID
        self.fullName = fullName
        self.shortName = shortName
        self.skillType = skillType
        self.additional_info = additionalInfo
        self.pass_requirement = passReq
        self.is_abstract = is_abstract

        self.parent = []
        self.children = []
        self.mastered = False


    def __eq__(self, other):
        """
        Needed to implement the verification of prerequisite
        :param other: the object to compare
        :return: true if self === other
        """
        if not isinstance(other, SkillTreeNode):
            return False
        return (self.ID == other.ID) and (self.shortName == other.shortName) and (self.fullName == other.fullName)

    def __str__(self):
        """
        The representation to be shown in a printed graph
        :return: a string containing key identification part of this node
        """
        return "[SKILL " + self.ID + ":" + self.shortName + "]"

    def pretty_print_with_height(self):
        """
        Pretty printing the node with formatting
        :return: list of printed str of the node, one for each line
        """
        if self.is_leaf():
            return [str(self)+"--LEAF"]

        front_spacing = (len(str(self)) + 1) * " "
        ret_list = [str(self) + ":/---"]
        for child in self.children:
            for line in child.pretty_print_with_height():
                ret_list.append(front_spacing + line)
        ret_list.append(front_spacing + "\---")
        return ret_list

    def add_parent(self, parent):
        """
        Add a parent to the representations
        :param parent: the SkillTreeNode to be added
        :return: None
        """
        if isinstance(parent, SkillTreeNode):
            self.parent.append(parent)
        else:
            raise Exception("Parent must be a SkillTreeNode")

    def get_parent(self):
        """
        Getter of the parent representation
        :return: parent
        """
        return self.parent

    def get_child(self):
        """
        Getter of the child representation
        :return: child
        """
        return self.children

    def remove_parent(self, parent):
        """
        Remove the parent if it is in the representation
        :param parent: the skillTreeNode to be removed
        :return: None
        """
        if not isinstance(parent, SkillTreeNode):
            raise Exception("Parent to be removed must be a SkillTreeNode")
        if parent in self.parent:
            self.parent.remove(parent)

    def add_child(self, child):
        """
        Add a child to the representations
        :param child: the skillTreeNode to be added
        :return: None
        """
        if isinstance(child, SkillTreeNode):
            self.children.append(child)
        else:
            raise Exception("Child must be a SkillTreeNode")

    def remove_child(self, child):
        """
        Remove the child if it is in the representation
        :param child: SkillTreeNode to be removed
        :return: None
        """
        if not isinstance(child, SkillTreeNode):
            raise Exception("Parent to be removed must be a SkillTreeNode")
        if child in self.children:
            self.children.remove(child)

    def get_full_name(self):
        """
        The getter of the name
        :return: name
        """
        return self.fullName

    def is_mastered(self):
        """
        Getter of the mastered
        :return: mastered
        """
        pass

    def get_is_abstract(self):
        """
        Getter of the is_abstract
        :return: is_abstract
        """
        pass

    def try_to_pass(self, your_result):
        """
        Compare your result to the pass requirements, if passed then return True and modify the mastered status
        :param your_result: your result to be judged
        :return: True if this skill is considered mastered and False otherwise
        """
        pass

    def is_leaf(self):
        """
        Judge whether this node is a leaf node
        :return: True if the child list is empty, False otherwise
        """
        return len(self.children) == 0