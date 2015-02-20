#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import unittest
import defpass


class TestParser(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.cf = defpass.CryptoFile()
         #cf = defpass.CryptoFile()


    def test_encrypt_file_with_invalid_folder(self):
        'Не существующий путь'
        self.cf.encrypt_file('/tmp-0')

    def test_decrypt_file_with_invalid_folder(self):
        'Несуществующий путь2'
        self.cf.decrypt_file('/tmp-0')

    def test_create_file_with_invalid_folder(self):
        'Несуществующий путь3'
        self.cf.create_new_defaulf_pass_file('/tmp-0', None)


if __name__ == '__main__':
    unittest.main()