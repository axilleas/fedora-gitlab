#!/usr/bin/env python2

import urllib2
#import subprocess

def gitlab_gems_list():
    '''url strings -> list

    Returns a sorted list of Gitlab's dependencies included in Gemfile.lock.

    '''
    gemfile_gitlab = urllib2.urlopen('https://raw.github.com/gitlabhq/gitlabhq/master/Gemfile.lock')
    gemfile_gitlab_shell = urllib2.urlopen('https://raw.github.com/gitlabhq/gitlab-shell/master/Gemfile.lock')

    gem_gitlab = gemfile_gitlab.readlines()
    gem_shell = gemfile_gitlab_shell.readlines()

    gems = []
    gems = gem_gitlab + gem_shell

    gitlab_gemlist = set()

    for line in gems:
        if line.startswith('    '):
            gitlab_gemlist.add(line.split()[0])
    
    return sorted(gitlab_gemlist)

def fedora_gems_list(fedora_gems_file):
    '''file -> list

    Returns a list of rubygems currently packaged in Fedora
    '''
    
    f = open(fedora_gems_file, 'r')
    gemlist = f.read().split('\n')
    f.close()

    return gemlist
    
def common_gems(gitlab_gemlist, fedora_gemlist):
    ''' lists -> set

    Returns a set of common gems between Gitlab and Fedora.

    >>> common_gems(['sinatra', 'sidekiq', 'sass_rails', 'sass'],['sass', 'rspec', 'sass_rails'])
    set(['sass_rails', 'sass'])
    '''
    
    return set(gitlab_gemlist) & set(fedora_gemlist)


def statistics(gitlab_gemlist, fedora_gemlist):
    '''
    '''
    pass

def main():
    #subprocess.call(['rubysearch.sh'], cwd='/home/axil/tools/fedora-gitlab/')
    gitlab_gems = gitlab_gems_list()
    fedora_gems_file = '/home/axil/tools/fedora-gitlab/rubygems_fedora'
    fedora_gems = fedora_gems_list(fedora_gems_file)
    common = common_gems(gitlab_gems, fedora_gems)

    #to_file = raw_input('Save Gitlab\'s deps as: ')
    to_file = '/home/axil/tools/fedora-gitlab/rubygems_gitlab'
    f = open(to_file, 'w')
    for rubygem in gitlab_gems:  
        f.write(rubygem + '\n')
    f.close()
    
    print 'Gitlab uses', len(gitlab_gems), 'gems.'
    print 'Fedora has packaged', len(fedora_gems), 'gems.'
    print 'There are', len(common), 'common gems.'
    print 'There should be packaged', len(gitlab_gems) - len(common), 'gems.'
    print 'Fedora will have', round((len(gitlab_gems) - len(common))/float(len(fedora_gems))*100,2), '% more ruby packages, that is', len(common)+len(fedora_gems), 'gems in total.'
    #for i in common:
    #    print i
if __name__ == '__main__':
    main()
