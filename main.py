import functools
from itertools import zip_longest
import re


@functools.total_ordering
class Version:

    def __init__(self, version):
        self.version = ((".".join(version.split('-'))).split('.'))
        self.base_version = self.version[:3]
        self.minor_version = self.version[3:]

    @staticmethod
    def __refactor(part):
        pattern = r'[a-z]+|\d+'
        separated_part = re.findall(pattern, part)
        return separated_part

    @staticmethod
    def __compare(version1, version2, fill_value='0'):
        """
        Comparator starts, not equal digits are compared as ascii digits,
        not equal chars are compared as ascii_letters (in respect that 'a' is equal to 'alpha', 'b' is equal to 'beta' ,
         'r' is equal to 'rc' etc.)
        If version consist of letters and numbers (for example, '4b' compared with '10'), __compare function is
        called again with this params.
        If comparator failed (versions are equal), None is returned

        :param version1:
        :param version2:
        :param fill_value:
        :return:
        """
        compared_list = Version.__zip(version1, version2, fill_value=fill_value)
        base_check = None
        for (value1, value2) in compared_list:
            if value1.isdigit() and value2.isdigit():
                if int(value1) != int(value2):
                    return int(value1) > int(value2)
            elif value1.isalpha() and value2.isalpha():
                if value1[0] != value2[0]:
                    return value1[0] > value2[0]
            else:
                temp_value_1 = Version.__refactor(value1)
                temp_value_2 = Version.__refactor(value2)
                return Version.__compare(temp_value_1, temp_value_2, fill_value='z')
        return base_check

    def __eq__(self, other):
        _equality = True

        if not isinstance(other, Version):
            return NotImplemented

        for (value1, value2) in self.__zip(self.version, other.version):
            if value1 != value2:
                _equality = False
                break
        return _equality

    def __gt__(self, other):
        """
        Basic approach is to compare versions bases, if they are equal, and base_compare_result is None,
        versions minor_versions are compared
        :param other:
        :return:
        """
        if not isinstance(other, Version):
            return NotImplemented

        base_compare_result = Version.__compare(self.base_version, other.base_version)
        if base_compare_result is None:
            return Version.__compare(self.minor_version, other.minor_version, fill_value='z')
        return base_compare_result

    @staticmethod
    def __zip(version1, version2, fill_value='0'):
        return list(zip_longest(version1, version2, fillvalue=fill_value))


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.4b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), 'le failed'
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()

