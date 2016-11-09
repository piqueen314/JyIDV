import sys
import os
idvjar=os.path.join(os.environ['IDV_HOME'],"idv.jar")
visadjar=os.path.join(os.environ['IDV_HOME'],"visad.jar")
sys.packageManager.addJar(idvjar,True)
sys.packageManager.addJar(visadjar,True)
sys.add_package('visad')
sys.add_package('visad.python')
sys.add_package('visad.data.units')
sys.add_package('ucar')
sys.add_package('ucar.unidata.idv')
sys.add_package('ucar.unidata.idv')
sys.add_package('ucar.unidata.ui')

import java

import visad
import visad.python
from visad import *
from visad.python.JPythonMethods import *
import ucar
from java.util import ArrayList
#idv=ucar.unidata.idv.IntegratedDataViewer(0)
idv=ucar.unidata.idv.DefaultIdv([])
IdvUIM=idv.getIdvUIManager()

import ucar.unidata.data.grid.GridUtil as GridUtil
import ucar.unidata.data.DataSelection as DataSelection
import ucar.unidata.data.GeoLocationInfo as GeoLocationInfo
import ucar.unidata.data.GeoSelection as GeoSelection

from ucar.unidata.idv.ui import ImageGenerator

from ucar.unidata.data import *
from ucar.unidata.idv import *
from ucar.unidata.data.grid import *
from java.lang import Integer
import ucar.unidata.data.grid.GridMath as GridMath
import ucar.unidata.data.DataUtil as DataUtil
import ucar.visad.Util as Util
import ucar.unidata.util.StringUtil as StringUtil
import ucar.unidata.data.grid.DerivedGridFactory as DerivedGridFactory
import ucar.unidata.data.grid.GridTrajectory as GridTrajectory

islInterpreter=ImageGenerator(idv)
JM=idv.getJythonManager()
LibHolders=JM.getLibHolders()
for i in range(len(LibHolders)):
    try:
        exec(LibHolders.get(i).getText())
    except:
        pass


def saveFormula(formulaid,desc,formula="",group=None):
    """ This function makes a IDV formula from jython script and puts it in relavent group
    in IDV list of formulas """
    # to do to check if function used in formula is legal/available
    from ucar.unidata.data import DerivedDataDescriptor,DataCategory
    from java.util import ArrayList
    JM=idv.getJythonManager()
    if not formulaid == None or not desc== None:
        if isinstance(group,list):
            for gr in group:
                categories=ArrayList()
                categories.add(DataCategory.parseCategory(gr,True))
                JM.addFormula(DerivedDataDescriptor(idv.getIdv(),formulaid,desc,formula,categories))
        else:
            group=str(group)
            categories=ArrayList()
            categories.add(DataCategory.parseCategory(group,True))
            JM.addFormula(DerivedDataDescriptor(idv.getIdv(),formulaid,desc,formula,categories))

def showImg(width=None,height=None):
    """ This function shows the image from current IDV frame, optional arguments are width and height in pixels, they
    currently default to 400 and 300"""
    from java.util import Base64 ##only in java8
    from javax.imageio import ImageIO
    from java.io import ByteArrayOutputStream
    from ucar.unidata.ui.ImageUtils import resize,toBufferedImage
    pause()
    #imgx=getImage() currently not working with new changes to idv
    img=idv.getViewManager().getMaster().getImage(True)
    if width != None and height != None:
        img=toBufferedImage(resize(img,width,height));
    bos=ByteArrayOutputStream();
    ImageIO.write(img, "png", Base64.getEncoder().wrap(bos));
    data = bos.toString("UTF-8");
    return {"display":"image","data":data}

def showImgWithFullWindow(width=None,height=None):
    """ This function shows the image from current IDV window while in GUI mode. optional arguments are width and height in pixels, they
    currently default to 600 and 400"""
    from java.util import Base64 ##only in java8
    from javax.imageio import ImageIO
    from java.io import ByteArrayOutputStream
    from ucar.unidata.ui.ImageUtils import resize,toBufferedImage
    import java
    import java.awt.Robot as Robot
    import java.awt.Rectangle as Rectangle
    import java.awt.Toolkit as Toolkit
    from ucar.unidata.util import Misc
    VM=idv.getViewManager()
    myframe=VM.getDisplayWindow().getComponent()
    robotx = Robot(myframe.getGraphicsConfiguration().getDevice())
    VM.toFront();
    #robotx.delay(250)
    Misc.sleep(350)
    pause()
    img=robotx.createScreenCapture(Rectangle( myframe.getX(),myframe.getY(),myframe.getWidth(),myframe.getHeight()))
    if width != None and height != None:
        img=toBufferedImage(resize(img,width,height));
    bos=ByteArrayOutputStream();
    ImageIO.write(img, "png", Base64.getEncoder().wrap(bos));
    data = bos.toString("UTF-8");
    return {"display":"image","data":data}

def showImgWithLegend(width=None,height=None):
    """ This function shows the image and legend from current IDV window while in GUI mode. Optional arguments are width and height in pixels, they currently default to 600 and 400"""
    from java.util import Base64 ##only in java8
    from javax.imageio import ImageIO
    from java.io import ByteArrayOutputStream
    from ucar.unidata.ui.ImageUtils import resize,toBufferedImage
    import java
    import java.awt.Robot as Robot
    import java.awt.Rectangle as Rectangle
    import java.awt.Toolkit as Toolkit
    from ucar.unidata.util import Misc
    VM=idv.getViewManager()
    VMC=VM.getContents()
    VMCC=VMC.getComponent(1) # the view and legend ; 0 is left most part of view window with controls for perspective views
    siz=VMCC.getSize()
    loc= VMCC.getLocationOnScreen()
    gc= VMCC.getGraphicsConfiguration()
    loc.x -= gc.getBounds().x
    loc.y -= gc.getBounds().y
    robotx=Robot(gc.getDevice())
    VM.toFront()
    Misc.sleep(250)
    img = robotx.createScreenCapture(Rectangle(loc.x, loc.y,siz.width, siz.height))
    if width != None and height != None:
        img=toBufferedImage(resize(img,width,height));
    bos=ByteArrayOutputStream();
    ImageIO.write(img, "png", Base64.getEncoder().wrap(bos));
    data = bos.toString("UTF-8");
    return {"display":"image","data":data}

def BufferedImgToNotebook(img):
    from java.io import ByteArrayOutputStream
    from java.util import Base64 ##only in java8
    from javax.imageio import ImageIO
    bos=ByteArrayOutputStream();
    ImageIO.write(img, "png", Base64.getEncoder().wrap(bos));
    data = bos.toString("UTF-8");
    return {"display":"image","data":data}

def showIdv(default=False):
    """ This creates a new IDV GUI window for showing after setOffScreen was True, after this GUI window of
    IDV is visible to the user, reset setOffScreen to False to go back into offscreen mode."""
    setOffScreen(False)
    #idv=ucar.unidata.idv.IntegratedDataViewer(True)
    idv=ucar.unidata.idv.DefaultIdv([])

    #IdvUIM=idv.getIdvUIManager()
    #IdvUIM.initDone()
    #IdvUIM.closeHelpTips()
    if default==True:
       if os.path.isfile(os.path.join(str(idv.getResourceManager().getUserPath()),"default.xidv")):
           loadBundle(os.path.join(str(idv.getResourceManager().getUserPath()),"default.xidv"))
       elif not len(idv.history) == 0:
           for hf in idv.history:
               if str(hf.getName()).endswith(".xidv"):
                   loadBundle(str(hf.getName()))
                   break
def saveJython(func=None,libname=None):
    """ This function saves history of interactive session to IDV Jython Library.
    When supplied by a defined class/function argument saves the code relavent to that class/function only
    When supplied by second string argument it creates library from that name or write to exisiting library by that
    name, only if it is editable by current user."""
    try:
       from org.python.core import PyFunction
       from org.python.core import PyClass
       from ucar.unidata.util import IOUtil
       import os
       import readline
       from random import randint

       pythonDir = IOUtil.joinDir(idv.getStore().getUserDirectory().toString(),"python")

       if (libname == None):
          libname="temp_"+str(randint(1000,9999))

       fullname = IOUtil.cleanFileName(libname)

       if not fullname.endswith(".py"):
          fullname = fullname + ".py"

       fullname = IOUtil.joinDir(pythonDir,fullname) # this takes care of type of slash based on os

       if os.path.exists(str(fullname)):
          raise Exception("A file with library name "+str(libname)+" already exists")

       if func==None:
           readline.write_history_file(str(fullname))
       elif isinstance(func,PyFunction) or isinstance(func,PyClass): #can get rid of this else if pass is used above
           readline.write_history_file("temp.txt")
           funcname=func.__name__
           ## ad-hoc matching use regex for robust matching
           if isinstance(func,PyFunction):
               funcname="def "+funcname+"("
           elif isinstance(func,PyClass):
               funcname="class "+funcname+"("
           fread=open("temp.txt").read()
           fnameindx=fread.rindex(funcname)
           #fnameindx=fread[:fnameindx].rindex('def')
           prevIndt=None
           functxt=[]
           for ln,line in enumerate(fread[fnameindx:].splitlines()):
               currIndt=len(line)-len(line.lstrip())
               if prevIndt<=currIndt or prevIndt==None:
                   functxt.append(line)
               else:
                   break
               prevIndt=currIndt
           f=open(str(fullname),"w")
           f.write('\n'.join(functxt))
           f.close()
       else:
           raise Exception("Unknown Error saving to IDV Jython library")
    except Exception as exc:
       return "Could not create a IDV Jython library: ",exc
idvBaseUrl=None
region=None
port=idv.getProperty('idv.monitorport','')

def pingIdv():
    import urllib
    global idvBaseUrl
    global port
    global region 
    try:
        idvBaseUrl="http://localhost:"+port
        return  urllib.urlopen(idvBaseurl+"/ping").read();
    except IOError:
        idvBaseUrl="http://127.0.0.1:"+port
        return  urllib.urlopen(idvbaseurl+"/ping").read();
    finally:
        return None
def runIsl(islcode):
    import urllib
    global idvBaseUrl
    pingIdv()
    if idvBaseUrl==None:
        return "Error connot connect to the IDV check your IDV version, only works for IDV > 5.3u1"
    else:
        urllib.urlopen(idvBaseUrl+"/loadisl?"+urllib.urlencode({'isl':islcode})).read()
        #return None
def loadBundleBB(fileName,north,south,east,west):
    isl=str('<isl><bundle file="'+str(fileName)+'" /><pause /><center north="'+str(north)+'" west="'+str(west)+'" south="'+str(south)+'" east="'+str(east)+'" /></isl>') 
    runIsl(isl)
    idv.getDataManager().reloadAllDataSources()

def do_complete(text):
    """Does code completion"""
    import __main__
    import __builtin__
    import readline
    import rlcompleter
    matchDict=__main__.__dict__.copy()
    matchDict.update(__builtin__.globals())
    rlc=rlcompleter.Completer(matchDict)
    rlc.complete(text,0)
    return list(set(rlc.matches)) #just to get rid of duplicates
def do_inspect(text):
    """ returns help like object """
    import pydoc
    try:
        token=text.split()[-1]
        if '(' in token:   #better do regex
           token=token[:-1]
        obj=eval(token)
        ins=pydoc.plain(pydoc.render_doc(obj))
        return ins
    except NameError:
        pass

def docHTML(text):
    """ just testing """
    import pydoc
    try:
        token=text.split()[-1]
        if '(' in token:   #better do regex
           token=token[:-1]
        obj=eval(token)
        #pyobj,name=pydoc.resolve(obj,0)
        ins=pydoc.plain(pydoc.render_doc(obj))
        html=pydoc.HTMLDoc()
        return html.page(pydoc.describe(obj), html.document(obj, name))
    except NameError:
        pass
def help(text):
    return "Use of help from notebook is currently unsupported, use SHIFT+TAB at end of the object you need help."
