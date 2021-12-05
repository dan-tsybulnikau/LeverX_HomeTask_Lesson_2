import string


class Version:

    def __init__(self, version):
        self.version = (".".join(version.split('-'))).split('.')

    @staticmethod
    def __compare(version1, version2):
        result_true, result_false = 1, 0
        if len(version1) == len(version2):
            pass
        elif len(version1) > len(version2):
            version2.extend(['0'] * (len(version1) - len(version2)))
        elif len(version2) > len(version1):
            version1.extend(['0'] * (len(version2) - len(version1)))
        for _ in range(len(version1)):

            if _ >= 3:
                if version1[_] == '0' or version2[_] == '0':
                    result_true, result_false = result_false, result_true
            else:
                version1[_] = ''.join([x for x in version1[_] if x not in string.ascii_letters])
                version2[_] = ''.join([x for x in version2[_] if x not in string.ascii_letters])
            if version1[_] > version2[_]:
                return result_true
            elif version2[_] > version1[_]:
                return result_false

    def __eq__(self, other):
        _equality = False
        if len(self.version) == len(other.version):
            for _ in range(len(self.version)):
                if self.version[_] != other.version[_]:
                    break
            else:
                _equality = True
        return _equality

    def __gt__(self, other):
        return True if Version.__compare(self.version, other.version) else False

    def __ge__(self, other):
        return Version.__eq__(self, other) or Version.__gt__(self, other)

    def __lt__(self, other):
        return False if Version.__compare(self.version, other.version) else True

    def __le__(self, other):
        return Version.__eq__(self, other) or Version.__lt__(self, other)


def main():

    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()
