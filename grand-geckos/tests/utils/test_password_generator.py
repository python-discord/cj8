import string
import pytest

from grand_geckos.utils import generate_passphrase, generate_password


class TestGeneratePassword:
    def test_length_zero(self):
        with pytest.raises(Exception):
            generate_password(length=0,
                              use_letters=True,
                              use_numbers=True,
                              use_symbols=False,
                              custom_letters="")

    def test_length_two(self):
        with pytest.raises(Exception):
            generate_password(length=2,
                              use_letters=True,
                              use_numbers=True,
                              use_symbols=False,
                              custom_letters="")

    def test_numbers(self):
        pw = generate_password(length=16,
                               use_letters=False,
                               use_numbers=True,
                               use_symbols=False,
                               custom_letters="")
        assert len(pw) == 16
        assert all(char.isdigit() for char in pw)

    def test_numbers_shortest(self):
        pw = generate_password(length=1,
                               use_letters=False,
                               use_numbers=True,
                               use_symbols=False,
                               custom_letters="")
        assert len(pw) == 1
        assert all(char.isdigit() for char in pw)

    def test_strings(self):
        pw = generate_password(length=16,
                               use_letters=True,
                               use_numbers=False,
                               use_symbols=False,
                               custom_letters="")
        assert len(pw) == 16
        assert any(char in string.ascii_lowercase for char in pw)
        assert any(char in string.ascii_uppercase for char in pw)
        assert all(char in string.ascii_letters for char in pw)

    def test_strings_shortest(self):
        pw = generate_password(length=2,
                               use_letters=True,
                               use_numbers=False,
                               use_symbols=False,
                               custom_letters="")
        assert len(pw) == 2
        assert all(char in string.ascii_letters for char in pw)

    def test_punctuations(self):
        pw = generate_password(length=16,
                               use_letters=False,
                               use_numbers=False,
                               use_symbols=True,
                               custom_letters="")
        assert len(pw) == 16
        assert all(char in string.punctuation for char in pw)

    def test_punctuations_shortest(self):
        pw = generate_password(length=1,
                               use_letters=False,
                               use_numbers=False,
                               use_symbols=True,
                               custom_letters="")
        assert len(pw) == 1
        assert all(char in string.punctuation for char in pw)

    def test_custom_letters(self):
        custom_letters = "¶|¼²°"
        pw = generate_password(length=16,
                               use_letters=False,
                               use_numbers=False,
                               use_symbols=False,
                               custom_letters=custom_letters)
        assert len(pw) == 16
        assert all(char in custom_letters for char in pw)

    def test_custom_letters_shortest(self):
        custom_letters = "¶|¼²°"
        pw = generate_password(length=1,
                               use_letters=False,
                               use_numbers=False,
                               use_symbols=False,
                               custom_letters=custom_letters)
        assert len(pw) == 1
        assert all(char in custom_letters for char in pw)

    def test_letters_numbers(self):
        pw = generate_password(length=16,
                               use_letters=True,
                               use_numbers=True,
                               use_symbols=False,
                               custom_letters="")
        assert len(pw) == 16
        assert any(char in string.ascii_lowercase for char in pw)
        assert any(char in string.ascii_uppercase for char in pw)
        assert any(char in string.digits for char in pw)
        assert all(char in string.ascii_letters + string.digits for char in pw)

    def test_letters_numbers_shortest(self):
        pw = generate_password(length=3,
                               use_letters=True,
                               use_numbers=True,
                               use_symbols=False,
                               custom_letters="")
        assert len(pw) == 3
        assert all(char in string.ascii_letters + string.digits for char in pw)

    def test_letters_numbers_impossible(self):
        with pytest.raises(Exception):
            generate_password(length=2,
                              use_letters=True,
                              use_numbers=True,
                              use_symbols=False,
                              custom_letters="")

    def test_letters_numbers_symbols(self):
        pw = generate_password(length=16,
                               use_letters=True,
                               use_numbers=True,
                               use_symbols=True,
                               custom_letters="")
        assert len(pw) == 16
        assert any(char in string.ascii_lowercase for char in pw)
        assert any(char in string.ascii_uppercase for char in pw)
        assert any(char in string.digits for char in pw)
        assert any(char in string.punctuation for char in pw)
        assert all(char in string.ascii_letters + string.digits + string.punctuation for char in pw)

    def test_letters_numbers_symbols_shortest(self):
        pw = generate_password(length=4,
                               use_letters=True,
                               use_numbers=True,
                               use_symbols=True,
                               custom_letters="")
        assert len(pw) == 4
        assert all(char in string.ascii_letters + string.digits + string.punctuation for char in pw)

    def test_letters_numbers_symbols_impossibe(self):
        with pytest.raises(Exception):
            generate_password(length=3,
                              use_letters=True,
                              use_numbers=True,
                              use_symbols=True,
                              custom_letters="")

    def test_letters_numbers_symbols_custom_letters(self):
        custom_letters = "¶|¼²°"
        pw = generate_password(length=16,
                               use_letters=True,
                               use_numbers=True,
                               use_symbols=True,
                               custom_letters=custom_letters)
        assert len(pw) == 16
        assert any(char in string.ascii_lowercase for char in pw)
        assert any(char in string.ascii_uppercase for char in pw)
        assert any(char in string.digits for char in pw)
        assert any(char in string.punctuation for char in pw)
        assert any(char in custom_letters for char in pw)
        assert all(char in string.ascii_letters + string.digits + string.punctuation + custom_letters for char in pw)

    def test_letters_numbers_symbols_custom_letters_shortest(self):
        custom_letters = "¶|¼²°"
        pw = generate_password(length=5,
                               use_letters=True,
                               use_numbers=True,
                               use_symbols=True,
                               custom_letters=custom_letters)
        assert len(pw) == 5
        assert all(char in string.ascii_letters + string.digits + string.punctuation + custom_letters for char in pw)

    def test_letters_numbers_symbols_custom_letters_impossibe(self):
        custom_letters = "¶|¼²°"
        with pytest.raises(Exception):
            generate_password(length=4,
                              use_letters=True,
                              use_numbers=True,
                              use_symbols=True,
                              custom_letters=custom_letters)


class TestGeneratePassphrase:
    def test_length_zero(self):
        with pytest.raises(Exception):
            generate_passphrase(length=0)

    def test_length_one(self):
        pw = generate_passphrase(length=1)
        pw_split = pw.split(" ")
        assert len(pw_split) == 1

    def test_length_two(self):
        pw = generate_passphrase(length=2)
        pw_split = pw.split(" ")
        assert len(pw_split) == 2

    def test_length_four(self):
        pw = generate_passphrase(length=4)
        pw_split = pw.split(" ")
        assert len(pw_split) == 4
