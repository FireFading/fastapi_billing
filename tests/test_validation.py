import pytest
from app.utils.validators import validate_name, validate_password


class TestPasswordValidation:
    def test_valid_password(self):
        password = "Test1234!"
        assert validate_password(password) == password

    def test_invalid_password(self):
        password = "invalidpassword"
        with pytest.raises(ValueError):
            validate_password(password)

    def test_password_less_than_min_length(self):
        password = "Short1!"
        with pytest.raises(ValueError):
            validate_password(password)

    def test_password_more_than_max_length(self):
        password = "ThisPasswordIsTooLong1234567890!"
        with pytest.raises(ValueError):
            validate_password(password)

    def test_password_no_lowercase(self):
        password = "PASSWORD1234!"
        with pytest.raises(ValueError):
            validate_password(password)

    def test_password_no_uppercase(self):
        password = "password1234!"
        with pytest.raises(ValueError):
            validate_password(password)

    def test_password_no_digit(self):
        password = "Password!"
        with pytest.raises(ValueError):
            validate_password(password)

    def test_password_no_punctuation(self):
        password = "Password1234"
        with pytest.raises(ValueError):
            validate_password(password)


class TestValidateName:
    def test_valid_name(self):
        name = "John Doe"
        assert validate_name(name) == name

    def test_empty_name(self):
        name = None
        assert validate_name(name) is None

    def test_name_less_than_min_length(self):
        name = "J"
        with pytest.raises(ValueError):
            validate_name(name)

    def test_name_more_than_max_length(self):
        name = "ThisNameIsTooLong" * 10
        with pytest.raises(ValueError):
            validate_name(name)

    def test_name_contains_only_spaces(self):
        name = "   "
        with pytest.raises(ValueError):
            validate_name(name)
