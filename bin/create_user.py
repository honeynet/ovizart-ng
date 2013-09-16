#!/usr/bin/env python
__author__ = 'ggercek'

import sys
sys.path.append('../')

from core import db
import argparse
import re


def main(args):

    def isEmailAddressValid(email):
        return re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

    def isEmpty(field):
        return field.strip() == ''

    def isArgumentsEmpty(args):
        fields = ['username', 'password', 'name', 'surname', 'email']
        _args = vars(args)
        for field in fields:
            if isEmpty(_args[field]):
                print '%s can not be empty. Please control your inputs.' % field
                return True

        return False

    returnCode = 1

    parser = argparse.ArgumentParser(description='Add new ovizart user')
    parser.add_argument('username', metavar='<username>')
    parser.add_argument('password', metavar='<password>')
    parser.add_argument('name', metavar='<name>')
    parser.add_argument('surname', metavar='<surname>')
    parser.add_argument('email', metavar='<email@example.com>')

    args = parser.parse_args(args)

    if not isArgumentsEmpty(args):
        # Test user name
        if db.getUserByName(args.username) is None:
            # No such user exists, it is ok to create a new one!!!
            # check email format
            if isEmailAddressValid(args.email):
                if db.addUser(args.username, args.password, args.name, args.surname, args.email):
                    print 'User created successfully.\nNow retrieving user for testing'
                    user = db.getUser(args.username, args.password)
                    if user:
                        print 'User retrieved successfully, user_id:', user
                        returnCode = 0
                    else:
                        print 'User can not be retrieved. Something went wrong.'
                        # TODO: add some explanation here.
                else:
                    print 'User can not be created. Please check whether mongo db is running or not!'
            else:
                print "Invalid email address! Please control your email address."
        else:
            print "Username already exists! Please select another username."
            # TODO: Update maybe added ?!

    sys.exit(returnCode)

if __name__ == '__main__':
    main(sys.argv[1:])