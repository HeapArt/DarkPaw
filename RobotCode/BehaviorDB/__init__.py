from os.path import dirname, basename, isfile, join, splitext
import glob

from .BehaviorDB import getBehaviorDB , addBehavior, BehaviorDB, gCreationCallback

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py') and not f.endswith('BehaviorDB.py')]


def _behaviorCreation(iRobot):

  wFilteredModules = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py') and not f.endswith('BehaviorDB.py')]

  for wModulePath in wFilteredModules:
    wFilename = basename(wModulePath)
    wModuleName = splitext(wFilename)[0]
    wEvalString = wModuleName + ".behaviorCreation(iRobot)"
    eval(wEvalString)

getBehaviorDB().subscribeToWakeCallback(_behaviorCreation)