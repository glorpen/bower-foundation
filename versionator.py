#!/usr/bin/env python3
import subprocess
import json
from verlib import NormalizedVersion as V, suggest_normalized_version
from collections import OrderedDict
from urllib.request import urlopen
import urllib
import os
import logging
from itertools import zip_longest

class CommandException(Exception):
    pass

class Versionator():
    def __init__(self):
        self.logger = logging.getLogger("Versionator")
        self.author = "mhayes"
        self.week_in_secs = 7*24*60*60
        self.commits_count = 10
        
    def _run_cmd(self, *args):
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        d = p.stdout.read()
        p.stdout.close()
        ret = p.wait()
        if(ret!=0):
            raise CommandException("Command returned %d" % ret)
        return d.decode()
    
    def _grep_by_week_or_count(self, tag, commits):
        """
        Returns list of versions per self.commits_count commits or self.week_in_secs
        """
        
        start = None
        release = 1
        i = 0
        grouped = []
        
        for c in commits:
            h, t = c.split(" ")
            t = int(t)
            
            if start is None:
                start = t
                continue
            
            i+=1
            
            if i > self.commits_count or t - start >= self.week_in_secs:
                grouped.append((h, self.normalize_version(tag+"-r%d"%release)))
                release+=1
                start = t
                i = 0
        
        return grouped
                
    
    def get_versions(self):
        tags = self._run_cmd("git","tag").splitlines()
        
        items = []
        
        for tag, tag_next in zip_longest(tags, tags[1:]):
            d = self._run_cmd("git","log", "%s...%s" % (tag, tag_next or ""), '--author=%s' % self.author, '--pretty=format:%H %ct').splitlines()
            if tag_next:
                d=d[1:]
            items.extend(self._grep_by_week_or_count(tag, reversed(d)))
        
        items.extend([(i, self.normalize_version(i)) for i in tags])
        
        items.sort(key=lambda x:V(x[1]), reverse=True)
        return OrderedDict(items)
    
    def check_pypi_version(self, version):
        
        #skip old releases
        if V(version) < V("4.3.2"):
            return True
    
        try:
            with urlopen("https://pypi.python.org/pypi/zurb-foundation/%s/json" % version) as f:
                f.read()
            return True
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False
            else:
                raise e
        
    def normalize_version(self, v):
        return suggest_normalized_version(v)
    
    def build_tag(self, tag, version):
        self._run_cmd("git", "checkout", "-f", "python")
        self._run_cmd("git", "clean", "-fd", "python")
        self._run_cmd("git", "checkout", "-f", tag, "scss", "js", "css")
        
        with open(os.path.join("python","__init__.py"), "r+t") as f:
            d = f.read().replace("%version%", str(version))
            f.seek(0)
            f.write(d)
            f.truncate()
        
        self.logger.info("building & uploading tag:%s version:%s", tag, version)
        self._run_cmd("rm","-rf","dist", "zurb_foundation.egg-info")
        self._run_cmd("python", "setup.py", "sdist", "upload")
        
    
    def run(self):
        self._run_cmd("git", "reset", "--hard")
        self._run_cmd("git", "checkout", "-f")
        self._run_cmd("git", "pull", "--no-edit", "https://github.com/zurb/bower-foundation.git")
        for tag, version in v.get_versions().items():
            if not self.check_pypi_version(version):
                self.build_tag(tag, version)
            else:
                #older ones should be already packed
                break


if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG)
    v = Versionator()
    v.run()
    
    """
    
    try:
        with open("key.txt","rt") as f:
            secret = f.read()
    except:
        secret = None
    
    from bottle import route, run

    @route('/<key>')
    def hook(key):
        
        if not (secret is None) and secret == key:
            try:
                v.run()
            except Exception as e:
                v.logger.error(e)
            
        return ''
    
    run(host='localhost', port=8080)
    """