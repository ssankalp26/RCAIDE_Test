## @ingroup Core
# redirect.py
#
# Created:  Aug 2015, T. Lukacyzk
# Modified: Feb 2016, T. MacDonald

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import os, sys, shutil, copy

# -------------------------------------------------------------------
#  Output Redirection 
# -------------------------------------------------------------------

## @ingroup Core
class output(object):
    """Redirects output to a file and folder

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    args   - Command to be evaluated
    folder - Location to store data

    Returns:
    None
    """
    def __init__(self, stdout=None, stderr=None):
        """ Initializes a new output() class
    
            Assumptions:
            N/A
    
            Source:
            N/A
    
            Inputs:
            N/A
    
            Outputs:
            N/A
    
            Properties Used:
            N/A    
        """         
        
        _newout = False
        _newerr = False
        
        if isinstance(stdout,str):
            stdout = open(stdout,'a')
            _newout = True            
        if isinstance(stderr,str):
            stderr = open(stderr,'a')
            _newerr = True                   
                
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr
        self._newout = _newout
        self._newerr = _newerr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush(); self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush(); self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        
        if self._newout:
            self._stdout.close()
        if self._newerr:
            self._stderr.close()           


# -------------------------------------------------------------------
#  Folder Redirection 
# -------------------------------------------------------------------

## @ingroup Core
class folder(object):
    """Creates a folder and outputs files to that folder

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    folder - Location to store data
    force  - Will remove the directory if it already exists

    Returns:
    None
    """
    
    def __init__(self, folder, pull=None, link=None, force=True ):
        ''' folder redirection initialization
            see help( folder ) for more info
        '''
        
        if pull is None: pull = []
        if link is None: link = []
        
        if not isinstance(pull,list) : pull = [pull]
        if not isinstance(link,list) : link = [link]
        
        origin = os.getcwd()
        origin = os.path.abspath(origin).rstrip('/')+'/'
        folder = os.path.abspath(folder).rstrip('/')+'/'
        
        self.origin = origin
        self.folder = folder
        self.pull   = copy.deepcopy(pull)
        self.push   = []
        self.link   = copy.deepcopy(link)
        self.force  = force

    def __enter__(self): 
        
        origin = self.origin  # absolute path
        folder = self.folder  # absolute path
        pull   = self.pull
        push   = self.push
        link   = self.link
        force  = self.force
        
        # check for no folder change
        if folder == origin:
            return []
        
        # check, make folder
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # copy pull files
        for name in pull:
            old_name = os.path.abspath(name)
            new_name = os.path.split(name)[-1]
            new_name = os.path.join(folder,new_name)
            if old_name == new_name: continue
            if os.path.exists( new_name ): 
                if force: os.remove( new_name )
                else: continue
            shutil.copy(old_name,new_name)

        # make links
        for name in link:
            old_name = os.path.abspath(name)
            new_name = os.path.split(name)[-1]
            new_name = os.path.join(folder,new_name)
            if old_name == new_name: continue
            if os.path.exists( new_name ): 
                if force: os.remove( new_name )
                else: continue
            make_link(old_name,new_name)
            
        # change directory
        os.chdir(folder)
        
        # return empty list to append with files to push to super folder
        return push

    def __exit__(self, exc_type, exc_value, traceback):
        
        origin = self.origin
        folder = self.folder
        push   = self.push
        force  = self.force
        
        # check for no folder change
        if folder == origin:
            return
        
        # move assets
        for name in push:
            
            old_name = os.path.abspath(name)
            name = os.path.split(name)[-1]
            new_name = os.path.join(origin,name)
            
            # links
            if os.path.islink(old_name):
                source = os.path.realpath(old_name)
                if source == new_name: continue
                if os.path.exists( new_name ):
                    if force: os.remove( new_name )
                    else: continue
                make_link(source,new_name)
            
            # moves
            else:
                if old_name == new_name: continue
                if os.path.exists( new_name ):
                    if force: os.remove( new_name )
                    else: continue
                shutil.move(old_name,new_name)
            
        # change directory
        os.chdir(origin)
        
  
def make_link(src,dst):
    """Makes a symbolic link

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    src - source location
    dst - destination location

    Returns:
    None
    """
    
    assert os.path.exists(src) , 'source file does not exist \n%s' % src
    
    if os.name == 'nt':
        # can't make a link in windows, need to look for other options
        if os.path.exists(dst): os.remove(dst)
        shutil.copy(src,dst)
    
    else:
        # find real file, incase source itself is a link
        src = os.path.realpath(src) 
        
        # normalize paths
        src = os.path.normpath(src)
        dst = os.path.normpath(dst)        
        
        # check for self referencing
        if src == dst: return        
        
        # find relative folder path
        srcfolder = os.path.join( os.path.split(src)[0] ) + '/'
        dstfolder = os.path.join( os.path.split(dst)[0] ) + '/'
        srcfolder = os.path.relpath(srcfolder,dstfolder)
        src = os.path.join( srcfolder, os.path.split(src)[1] )
        
        # make unix link
        if os.path.exists(dst): os.remove(dst)
        os.symlink(src,dst)
    