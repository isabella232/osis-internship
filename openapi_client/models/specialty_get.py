# coding: utf-8

"""
    Internship API

    This API delivers data for the Internship project.  # noqa: E501

    OpenAPI spec version: 1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class SpecialtyGet(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'uuid': 'str',
        'name': 'str',
        'acronym': 'str',
        'mandatory': 'bool',
        'sequence': 'float',
        'cohort': 'object',
        'selectable': 'bool'
    }

    attribute_map = {
        'uuid': 'uuid',
        'name': 'name',
        'acronym': 'acronym',
        'mandatory': 'mandatory',
        'sequence': 'sequence',
        'cohort': 'cohort',
        'selectable': 'selectable'
    }

    def __init__(self, uuid=None, name=None, acronym=None, mandatory=None, sequence=None, cohort=None, selectable=None):  # noqa: E501
        """SpecialtyGet - a model defined in OpenAPI"""  # noqa: E501

        self._uuid = None
        self._name = None
        self._acronym = None
        self._mandatory = None
        self._sequence = None
        self._cohort = None
        self._selectable = None
        self.discriminator = None

        if uuid is not None:
            self.uuid = uuid
        if name is not None:
            self.name = name
        if acronym is not None:
            self.acronym = acronym
        if mandatory is not None:
            self.mandatory = mandatory
        if sequence is not None:
            self.sequence = sequence
        if cohort is not None:
            self.cohort = cohort
        if selectable is not None:
            self.selectable = selectable

    @property
    def uuid(self):
        """Gets the uuid of this SpecialtyGet.  # noqa: E501


        :return: The uuid of this SpecialtyGet.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this SpecialtyGet.


        :param uuid: The uuid of this SpecialtyGet.  # noqa: E501
        :type: str
        """

        self._uuid = uuid

    @property
    def name(self):
        """Gets the name of this SpecialtyGet.  # noqa: E501


        :return: The name of this SpecialtyGet.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SpecialtyGet.


        :param name: The name of this SpecialtyGet.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def acronym(self):
        """Gets the acronym of this SpecialtyGet.  # noqa: E501


        :return: The acronym of this SpecialtyGet.  # noqa: E501
        :rtype: str
        """
        return self._acronym

    @acronym.setter
    def acronym(self, acronym):
        """Sets the acronym of this SpecialtyGet.


        :param acronym: The acronym of this SpecialtyGet.  # noqa: E501
        :type: str
        """

        self._acronym = acronym

    @property
    def mandatory(self):
        """Gets the mandatory of this SpecialtyGet.  # noqa: E501


        :return: The mandatory of this SpecialtyGet.  # noqa: E501
        :rtype: bool
        """
        return self._mandatory

    @mandatory.setter
    def mandatory(self, mandatory):
        """Sets the mandatory of this SpecialtyGet.


        :param mandatory: The mandatory of this SpecialtyGet.  # noqa: E501
        :type: bool
        """

        self._mandatory = mandatory

    @property
    def sequence(self):
        """Gets the sequence of this SpecialtyGet.  # noqa: E501


        :return: The sequence of this SpecialtyGet.  # noqa: E501
        :rtype: float
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this SpecialtyGet.


        :param sequence: The sequence of this SpecialtyGet.  # noqa: E501
        :type: float
        """

        self._sequence = sequence

    @property
    def cohort(self):
        """Gets the cohort of this SpecialtyGet.  # noqa: E501


        :return: The cohort of this SpecialtyGet.  # noqa: E501
        :rtype: object
        """
        return self._cohort

    @cohort.setter
    def cohort(self, cohort):
        """Sets the cohort of this SpecialtyGet.


        :param cohort: The cohort of this SpecialtyGet.  # noqa: E501
        :type: object
        """

        self._cohort = cohort

    @property
    def selectable(self):
        """Gets the selectable of this SpecialtyGet.  # noqa: E501


        :return: The selectable of this SpecialtyGet.  # noqa: E501
        :rtype: bool
        """
        return self._selectable

    @selectable.setter
    def selectable(self, selectable):
        """Sets the selectable of this SpecialtyGet.


        :param selectable: The selectable of this SpecialtyGet.  # noqa: E501
        :type: bool
        """

        self._selectable = selectable

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SpecialtyGet):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
