# -*- coding: utf-8 -*-
'''
Подготовка файлов перед выпуском новой версии
 
@file prepare-install.py
@author aleksey.hohryakov@gmail.com
'''

import ConfigParser
import hashlib
import os
import shutil
import sys
from subprocess import call

qtsdkPath = 'c:\\QtSDK\\Desktop\\Qt\\4.8.0\\mingw'
quiterssSourcePath = "e:\\Work\\_Useful\\QtProjects\\QuiteRSS"
quiterssReleasePath = "e:\\Work\\_Useful\\QtProjects\\QuiteRSS-build-desktop_Release\\release\\target"
updaterPath = "e:\\Work\\_Useful\\QtProjects\\QuiteRSS-build-desktop_Release\\release\\target"
preparePath  = "e:\\Work\\_Useful\\QtProjects\\QuiteRSS_prepare-install"
portablePath  = "e:\\Work\\_Useful\\QtProjects"
quiterssFileRepoPath = 'e:\\Work\\_Useful\\QtProjects\\QuiteRss.File'
packerPath = 'e:\\Work\\_Utilities\\7za\\7za.exe'
innoSetupCompilerPath = 'C:\\Program Files\\Inno Setup 5\\Compil32.exe'

# Список файлов состоит из относительного пути папки, содержащей файл,
# и имени файла, который необходимо скопировать
ID_DIR  = 0
ID_NAME = 1
filesFromSource = [
  ['\\sound', 'notification.wav'],
  ['', 'AUTHORS'],
  ['', 'COPYING'],
  ['', 'HISTORY_EN'],
  ['', 'HISTORY_RU'],
  ['', 'README'],
  ['', 'TODO']
]

filesFromRelease = [
  ['', 'QuiteRSS.exe']
]

filesFromUpdater = [
  ['', '7za.exe'],
  ['', 'Updater.exe']
]

filesFromQtSDKPlugins = [
  ['\\sqldrivers', 'qsqlite4.dll'],
  ['\\iconengines', 'qsvgicon4.dll'],
  ['\\imageformats', 'qgif4.dll'],
  ['\\imageformats', 'qico4.dll'],
  ['\\imageformats', 'qjpeg4.dll'],
  ['\\imageformats', 'qmng4.dll'],
  ['\\imageformats', 'qsvg4.dll'],
  ['\\imageformats', 'qtga4.dll'],
  ['\\imageformats', 'qtiff4.dll'],
  ['\\phonon_backend', 'phonon_ds94.dll']
]

filesFromQtSDKBin = [
  ['', 'libeay32.dll'],
  ['', 'libgcc_s_dw2-1.dll'],
  ['', 'libssl32.dll'],
  ['', 'mingwm10.dll'],
  ['', 'phonon4.dll'],
  ['', 'QtCore4.dll'],
  ['', 'QtGui4.dll'],
  ['', 'QtNetwork4.dll'],
  ['', 'QtSql4.dll'],
  ['', 'QtSvg4.dll'],
  ['', 'QtWebKit4.dll'],
  ['', 'QtXml4.dll'],
  ['', 'ssleay32.dll']
]

prepareFileList = []

def createPreparePath(path):
  print "---- Preparing path: " + path
  if (os.path.exists(path)):
    print "Path exists. Remove it"
    shutil.rmtree(path)
  
  os.makedirs(path)
  print "Path created"
    
def copyLangFiles():
  print "---- Copying language files..."
  
  shutil.copytree(quiterssReleasePath + "\\lang", preparePath + "\\lang")
  shutil.copystat(quiterssReleasePath + "\\lang", preparePath + "\\lang")
  
  global prepareFileList
  langFiles = os.listdir(preparePath + "\\lang")
  for langFile in langFiles:
    langPath = '\\lang\\' + langFile
    print langPath
    prepareFileList.append(langPath)
    
  print "Done"

def copyFileList(fileList, src):
  '''
  Копирование файлов из списка fileList из папки src
  '''
  print "---- Copying files from " + src
  
  global prepareFileList
  
  # Перебираем список файлов
  for file in fileList:
    print file[ID_DIR] + '\\' + file[ID_NAME]
    
    # Если есть имя папки, то создаём её
    if file[ID_DIR] and (not os.path.exists(preparePath + file[ID_DIR])):
      os.makedirs(preparePath + file[ID_DIR])
      
    # Копируем файл, обрабатывая ошибки
    try:
      shutil.copy2(src + file[ID_DIR] + '\\' + file[ID_NAME], preparePath + file[ID_DIR] + '\\' + file[ID_NAME])
    except (IOError, os.error), why:
      print str(why)
      
    prepareFileList.append(file[ID_DIR] + '\\' + file[ID_NAME])
    
  print "Done"

def createMD5(fileList, path):
  '''
  Формирование md5-файла
  '''
  print "---- Create md5-file for all files in " + path
  
  f = open(path + '\\file_list.md5', 'w')
  for file in fileList:
    fileName = path + file
    fileHash = hashlib.md5(open(fileName, 'rb').read()).hexdigest()
    line = fileHash + ' *' + file[1:]
    f.write(line + '\n')
    print line
    
  f.close()
  print "Done"

def copyMD5():
  print "---- Copying md5-file to quiterss.file-repo"
  shutil.copy2(preparePath + '\\file_list.md5', quiterssFileRepoPath + '\\file_list.md5')
  print "Done"

def packFiles(fileList, path):
  '''
  Пакуем каждый файл в индивидуальный архив
  '''
  print '---- Pack files'
  for file in fileList:
    packCmdLine = packerPath + ' a "' + path + file + '.7z" "' + path + file + '"'
    print 'subprocess.call(' + packCmdLine + ')'
    call(packCmdLine);
  
  print "Done"

def copyPackedFiles():
  print '---- Copying packed files to quiterss.file-repo.windows'
  
  prepareFileList7z = []
  for file in prepareFileList:
    prepareFileList7z.append(file + '.7z')
  
  for file in prepareFileList7z:
    print 'copying: ' + file
    shutil.copy2(preparePath + file, quiterssFileRepoPath + '\\windows' + file)
  
  print 'Done'

def updateFileRepo():
  print '---- Updating repo: ' + quiterssFileRepoPath
  
  callLine = 'hg commit --cwd "' + quiterssFileRepoPath + '"' \
      + ' --addremove --subrepos --message "update windows install files"'
  print 'call(' + callLine + ')'
  call(callLine)
  print ""
  
  callLine = 'hg log --cwd "' + quiterssFileRepoPath + '"' \
      + ' --verbose --limit 1'
  print 'call(' + callLine + ')'
  call(callLine)
  print ""
  
  callLine = 'hg push --cwd "' + quiterssFileRepoPath + '"'
  print 'call(' + callLine + ')'
  call(callLine)
  print ""
  
  print 'Done'

def readConfigFile():
  global qtsdkPath
  global quiterssSourcePath
  global quiterssReleasePath
  global updaterPath
  global preparePath
  global portablePath
  global quiterssFileRepoPath
  global packerPath
  
  configFileName = os.path.basename(sys.argv[0]).replace('.py', '.ini')
  print '---- Reading config file: ' + configFileName
  
  if (not os.path.exists(configFileName)):
    print 'Abort: file not found'
    return
  
  config = ConfigParser.SafeConfigParser()
  config.optionxform = str
  config.read(configFileName)
  print config.items('paths')

  qtsdkPath = config.get('paths', 'qtsdkPath')
  quiterssSourcePath = config.get('paths', 'quiterssSourcePath')
  quiterssReleasePath = config.get('paths', 'quiterssReleasePath')
  updaterPath = config.get('paths', 'updaterPath')
  preparePath = config.get('paths', 'preparePath')
  if (config.has_option('paths', 'portablePath')):
    portablePath = config.get('paths', 'portablePath')
  quiterssFileRepoPath = config.get('paths', 'quiterssFileRepoPath')
  packerPath = config.get('paths', 'packerPath')
  if (config.has_option('paths', 'innoSetupCompilerPath')):
    innoSetupCompilerPath = config.get('paths', 'innoSetupCompilerPath')

  print 'Done'

def writeConfigFile():
  configFileName = os.path.basename(sys.argv[0]).replace('.py', '.ini')
  print '---- Writing config file: ' + configFileName
  
  config = ConfigParser.SafeConfigParser()
  config.optionxform = str
  config.add_section('paths')
  config.set('paths', 'qtsdkPath', qtsdkPath)
  config.set('paths', 'quiterssSourcePath', quiterssSourcePath)
  config.set('paths', 'quiterssReleasePath', quiterssReleasePath)
  config.set('paths', 'updaterPath', updaterPath)
  config.set('paths', 'preparePath', preparePath)
  config.set('paths', 'portablePath', portablePath)
  config.set('paths', 'quiterssFileRepoPath', quiterssFileRepoPath)
  config.set('paths', 'packerPath', packerPath)
  config.set('paths', 'innoSetupCompilerPath', innoSetupCompilerPath)
  print config.items('paths')

  # Writing our configuration to file
  with open(configFileName, 'wb') as configfile:
    config.write(configfile)
  
  print 'Done'

def makePortableVersion():
  portableTempPath = portablePath + '\\QuiteRSS-' + '0.0.0'
  print '---- Makeing portable version in ' + portableTempPath

  if (os.path.exists(portableTempPath)):
    print "Path exists. Remove it"
    shutil.rmtree(portableTempPath)
  
  print 'Copying files...'
  shutil.copytree(preparePath, portableTempPath)
  shutil.copystat(preparePath, portableTempPath)
  
  print 'Creating portable.dat...'
  f = open(portableTempPath + '\\portable.dat', 'w')
  f.close()
  
  print 'Pack folder...'
  packCmdLine = packerPath + ' a "' + portableTempPath + '.7z" "' + portableTempPath + '"'
  print 'subprocess.call(' + packCmdLine + ')'
  call(packCmdLine);
  
  print 'Remove folder...'
  shutil.rmtree(portableTempPath)
  
  print 'Done'

def makeSources():
  sourcesTempPath = portablePath + '\\QuiteRSS-' + '0.0.0' + '-src'
  print '---- Making sources in ' + sourcesTempPath

  if (os.path.exists(sourcesTempPath)):
    print "Path exists. Remove it"
    shutil.rmtree(sourcesTempPath)

  if (os.path.exists(sourcesTempPath + '.tar.bz2')):
    print "File exists. Remove it"
    # shutil.rmtree(sourcesTempPath)
    os.remove(sourcesTempPath + '.tar.bz2')
  
  print 'Export mercurial sources...'
  packCmdLine = 'hg archive --cwd ' + quiterssSourcePath + ' --type tbz2 ' + sourcesTempPath + '.tar.bz2'
  print 'subprocess.call(' + packCmdLine + ')'
  call(packCmdLine);
  
  print 'Done'

def makeInstaller():
  print '---- Making installer...'
  quiterssFileDataPath = quiterssFileRepoPath + '\\installer\\Data'

  if (os.path.exists(quiterssFileDataPath)):
    print "Path ...\\installer\\Data exists. Remove it"
    shutil.rmtree(quiterssFileDataPath)
  
  print 'Copying files...'
  shutil.copytree(preparePath, quiterssFileDataPath)
  shutil.copystat(preparePath, quiterssFileDataPath)
  
  print 'Run Inno Setup compiler...'
  cmdLine = [innoSetupCompilerPath, '/cc', quiterssFileRepoPath + '\\installer\\quiterss.iss']
  print 'subprocess.call(' + str(cmdLine) + ')'
  call(cmdLine)
  
  print 'Copying installer...'
  shutil.copy2(quiterssFileRepoPath + '\\installer\\Setup\\QuiteRSS-' + '0.0.0' + '-Setup.exe', portablePath)
  
  print 'Cleanup installer files...'
  shutil.rmtree(quiterssFileRepoPath + '\\installer\\Data')
  shutil.rmtree(quiterssFileRepoPath + '\\installer\\Setup')
  
  print 'Done'

def main():
  print "QuiteRSS prepare-install"
  readConfigFile()
  createPreparePath(preparePath)
  copyLangFiles()
  copyFileList(filesFromRelease, quiterssReleasePath)
  copyFileList(filesFromUpdater, updaterPath)
  copyFileList(filesFromSource, quiterssSourcePath)
  copyFileList(filesFromQtSDKPlugins, qtsdkPath + '\\plugins')
  copyFileList(filesFromQtSDKBin, qtsdkPath + '\\bin')
  makePortableVersion()
  makeSources()
  makeInstaller()
  createMD5(prepareFileList, preparePath)
  copyMD5()
  packFiles(prepareFileList, preparePath)
  copyPackedFiles()
  if (len(sys.argv) < 2) or (sys.argv[1] != '--dry-run'):
    updateFileRepo()
  writeConfigFile()

if __name__ == '__main__':
  main()
