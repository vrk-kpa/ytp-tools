#! /usr/bin/env python

""" Simple script to replace packages on development machine """

import sys
import re
import types
import subprocess
import os
import shutil


class YtpDevelopMain(object):
    source_path = "/src"
    virtual_environment = "/usr/lib/ckan/default"
    _mappings = None

    def develop_ckanext(self, name):
        project_path = os.path.join(self.source_path, name)
        if not os.path.isdir(project_path):
            print "Failed to find project at %s" % project_path
            return 1

        subprocess.call([os.path.join(self.virtual_environment, "bin/pip"), "uninstall", "--yes", name])
        os.chdir(project_path)
        subprocess.call([os.path.join(self.virtual_environment, "bin/python"), "setup.py", "develop"])

        return 0

    def _replace_with_link(self, original_path, source_path):
        shutil.rmtree(original_path)
        os.symlink(source_path, original_path)
        return 0

    def develop_assets(self, name):
        return self._replace_with_link("/var/www/shared", "/src/ytp-assets-common/distribution")

    def develop_drupal(self, name):
        return self._replace_with_link("/var/www/ytp/sites/all/themes/ytp_theme", "/src/ytp-theme-drupal")

    def list_projects(self, name=None):
        for name in os.listdir(self.source_path):
            if os.path.isdir(os.path.join(self.source_path, name)) and self._get_mapping(name):
                print name
        return 0

    def paster_serve(self, name=None):
        subprocess.call(["/usr/sbin/ufw", "allow", "5000"])
        subprocess.call(["/usr/bin/sudo", "-u", "ckan", os.path.join(self.virtual_environment, "bin/paster"), "serve", "/etc/ckan/default/production.ini"])
        print "Failed to launch server"
        return 1  # exit via ctrl-c

    def _get_mappings(self):
        if self._mappings is None:
            self._mappings = {re.compile(u'^ckanext-.+'): self.develop_ckanext, u'ytp-assets-common': self.develop_assets,
                              u'ytp-theme-drupal': self.develop_drupal,
                              u'--list': self.list_projects, u'--serve': self.paster_serve}
        return self._mappings

    def _get_mapping(self, project_name):
        for matcher, method in self._get_mappings().iteritems():
            if type(matcher) in types.StringTypes:
                if matcher == project_name:
                    return method
            elif getattr(matcher, 'match', False):
                if matcher.match(project_name):
                    return method
        return None

    def main(self, arguments):
        if len(arguments) != 2:
            print u"Usage: %s <project-name>\n       %s --list\n       %s --serve" % (arguments[0], arguments[0], arguments[0])
            exit(2)

        project_name = arguments[1]
        method = self._get_mapping(project_name)
        if method:
            return method(project_name)

        print u"Failed to find method project name %s" % project_name
        exit(3)

if __name__ == '__main__':
    exit(YtpDevelopMain().main(sys.argv))
