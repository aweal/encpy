#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
from time import sleep
import gnupg
import logging
import argparse
import sys
import getpass


home_dir = os.path.expanduser('~') + '/'
gpg_home = home_dir + '.gnupg'
default_crypt_file = home_dir + '.bac/one.gpg'
editor = 'gedit '
recipient_name = 'aweal' #имя ключа

class CryptoFile():
    def __init__(self, lgr=None):
        self.gpg = gnupg.GPG(gnupghome=gpg_home)
        if not lgr is None:
            self.lgr = lgr
        else:
            #default logger
            logger = logging.getLogger('CrypToFileLogger')
            ch = logging.StreamHandler()
            formt = logging.Formatter('%(levelname)s - %(message)s')
            logger.setLevel(logging.ERROR)
            ch.setLevel(logging.ERROR)
            ch.setFormatter(formt)
            logger.addHandler(ch)
            self.lgr = logger

    def print_status(self, status, fine_name):
        if self.lgr is not None:
            self.lgr.debug('status ... %s ', status.status)

            if not status.ok:
                self.lgr.error('Error crypt / decrypt file `%s `', fine_name)
                self.lgr.error('Error msg: `%s `', status.stderr)
            else:
                self.lgr.debug('ok: %s', status.ok)
                self.lgr.debug('status: %s', status.status)
                self.lgr.debug('stderr: %s ', status.stderr)
                self.lgr.debug('')

    def encrypt_file(self, file_name):
        if os.path.isfile(file_name):
            file_out = file_name + '.gpg'
            with open(file_name, 'rb') as file_in:
                try:
                    status = self.gpg.encrypt_file(file_in,
                        recipients = [recipient_name], output=file_out)
                finally:
                    self.print_status(status, file_name)

            if status.ok:
                self.lgr.debug('Encrypt complete, delete file `%s`', file_name)
                try:
                    os.remove(file_name)
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    self.lgr.error('File was not deleted!')
            return status.ok
        else:
            self.lgr.error('No file to encrypt...')
            return False

    def decrypt_file(self, file_name=None):
        """
        возвращает имя дешифрованного файла или 0
        """
        if file_name is None:
            file_name = default_crypt_file
        if os.path.isfile(file_name):
            self.lgr.debug('open file...')
            file_out = os.path.splitext(file_name)[0]
            result = False
            pw = getpass.getpass()
            if pw:
                self.lgr.debug('Pass  is entered, decrypt file...')
                with open(file_name, 'rb') as file_in:
                    try:
                        status = self.gpg.decrypt_file(file_in,
                          passphrase=pw, output=file_out)
                    finally:
                        self.print_status(status, file_name)

                if status.ok:
                    if os.path.exists(file_out):
                        return file_out
            else:
                self.lgr.error('No password answer, exit ...')
                return False
        else:
            self.lgr.error('No file to decrypt `%s`', file_name)
            return False

    def decrypt_and_show(self, file_name=None):
        d_file_name = self.decrypt_file(file_name)

        if d_file_name:
            self.lgr.debug('Open decrypted file `%s`', d_file_name)
            with open(d_file_name, 'r') as df:
                lines = df.readlines()
                for _line in lines:
                    print(_line)
            try:
                sleep(30)
            except KeyboardInterrupt:
                self.lgr.debug('Exit and delete file:')
            finally:
                os.system('reset')
                try:
                    os.remove(d_file_name)
                except:
                    self.lgr.warning('cannot delete file `%s`!!!!', d_file_name)
                    self.lgr.debug('Error msg: %s', sys.exc_info()[0])

    def decrypt_and_edit(self, file_name=None):
        d_file_name = self.decrypt_file(file_name)
        if d_file_name:
            self.lgr.debug('Open decrypted file `%s`', d_file_name)
            os.system(editor + d_file_name)
            if self.encrypt_file(d_file_name):
                if os.path.exists(d_file_name):
                    try:
                        os.remove(d_file_name)
                    except:
                        self.lgr.warning('cannot delete file `%s`!!!!', d_file_name)
                        self.lgr.debug('Error msg: %s', sys.exc_info()[0])
            else:
                self.lgr.warning('Cannon encrypt file `%s`', d_file_name)

    def create_new_defaulf_pass_file(self, create_file_name, file_n):
        try:
            with open(create_file_name, 'w+') as new_file:
                self.lgr.debug('create new pass file: `%s`', file_n)
        except IOError:
            if file_n is None:
                if os.path.exists(home_dir):
                    self.lgr.debug('Create ~/.bac folder')
                    try:
                        os.makedirs(home_dir + '.bac/')
                    except:
                        self.lgr.error('Cannot create folder %s', home_dir + '.bac/')
                        self.lgr.error('Error msg: %s', sys.exc_info()[0])
                        return False
                    self.create_new_defaulf_pass_file(create_file_name, 'NotNull!!!')
        except:
            self.lgr.error('Error msg: %s', sys.exc_info()[0])
            return False
        else:
            logger.error('Failed open file `%s`', new_file_name)

if __name__=='__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-f',  '--filename', type=str, help='path to enc / decrypt file default'
                    + default_crypt_file)
    parser.add_argument('-d', '--decrypt', action='store_true', help='decrypt this file')
    parser.add_argument('-a', '--add', action='store_true', help='Edit with txt redactor')
    parser.add_argument('-e', '--encrypt', action='store_true', help='encrypt this file')
    parser.add_argument('-v', '--verbose', action='store_true', help='set verbose log-level')

    args = parser.parse_args()

    logger = logging.getLogger('CrypToFileLogger')
    ch = logging.StreamHandler()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
        formt = logging.Formatter('%(asctime)s - '
            '%(name)s - %(levelname)s - %(message)s')

    else:
        formt = logging.Formatter('%(levelname)s - %(message)s')
        logger.setLevel(logging.ERROR)
        ch.setLevel(logging.ERROR)

    ch.setFormatter(formt)
    logger.addHandler(ch)

    cf = CryptoFile(logger)

    logger.debug('debug lvl ;) ')
    logger.debug('args: %s', args)

    if args.add:
        cf.decrypt_and_edit(args.filename)
        exit(0)

    if args.decrypt:
        logger.debug('Start decrypt file: `%s` ...', args.filename)
        cf.decrypt_file(args.filename)
        exit(0)

    if args.encrypt:
        logger.debug('Start encrypt file: `%s` ...', args.filename)
        cf.encrypt_file(args.filename)
        exit(0)


    if args.filename is None:
        _file_name = default_crypt_file

    else:
        _file_name = args.filename

    logger.debug('Processing the default file: `%s`', _file_name)

    if not os.path.exists(_file_name):
        new_file_name = _file_name[:-4]
        cf.create_new_defaulf_pass_file(new_file_name, args.filename)

        if cf.encrypt_file(new_file_name):
            logger.debug('Edit new file ')
            cf.decrypt_and_edit()
        else:
            logger.error('Cannon encrypt `%s` file', new_file_name)

    else:
       cf.decrypt_and_show(_file_name)


