import os
import subprocess
import re
import urllib
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    This command to make easier push to github:
    you just run it in command line: =>
    python manage.py git_push -m 'your commit message'
    OR
    python manage.py git_push, and then you will see it "Enter commit message: "

    NOTE: !!!
    for git commit message don't use single quotes
    """
    def add_arguments(self, parser):
        parser.add_argument(
            '-m',
            dest='message',
            required=False,
            type=str
        )

    def handle(self, *args, **options):
        if not self.check_connection_internet():
            return self.stdout.write(
                self.style.ERROR_OUTPUT(
                    'Sorry, Please check your internet connection'
                )
            )
        commit_message = options['message']
        if not commit_message:
            commit_message = input('Enter commit message: ')
        os.system('git add .')
        os.system('git commit -m "%s"' % str(commit_message))
        os.system('git push origin %s' % self.get_branch())
        self.stdout.write(self.style.SUCCESS('\n\nSuccessfully push your work :D'))

    def get_branch(self):
        proc = subprocess.check_output(["git", "branch"])

        if isinstance(proc, bytes):
            proc = proc.decode('utf-8')

        branchs = proc.strip()
        if '\n' in proc:
            branchs = branchs.split('\n')

        if not isinstance(branchs, list):
            branchs = [branchs]

        cur_branch = None
        for branch in branchs:
            if re.match(r'[*]', branch):
                cur_branch = branch
                break

        if cur_branch:
            cur_branch = cur_branch.replace('*', '').strip()
        return cur_branch

    def check_connection_internet(self, host='http://google.com'):
        try:
            urllib.request.urlopen(host, timeout=1)
            return True
        except Exception:
            return False