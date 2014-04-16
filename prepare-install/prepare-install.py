# -*- coding: utf-8 -*-
'''
Подготовка файлов перед выпуском новой версии

@file prepare-install.py
@author aleksey.hohryakov@gmail.com
@author egor.shilyaev@gmail.com
'''

import ConfigParser
import hashlib
import os
import shutil
import sys
from subprocess import call

qtsdkPath = 'y:\\Qt\\Qt4.8.5'
mingwPath = 'y:\\Qt\\Qt4.8.4\\mingw'
quiterssSourcePath = 'd:\\Temp_D\\Project\\QuiteRSS'
quiterssBuildPath = 'd:\\Temp_D\\Project\\QuiteRSS-build-desktop'
quiterssReleasePath = 'd:\\Temp_D\\Project\\QuiteRSS-build-desktop\\release\\target'
updaterPath = 'd:\\Temp_D\\Project\\!QuiteRSS\\build-updater-Desktop\\release\\target'
preparePath = 'd:\\Temp_D\\Project\\!QuiteRSS\\prepare-install-build'
prepareBinPath = 'd:\\Temp_D\\Project\\!QuiteRSS\\prepare-install-build\\release'
packagesPath = 'd:\\Programming\\Version\\push'
testPackagesPath = 'd:\\Programming\\YandexDisk\\QuiteRSS-test'
quiterssFileRepoPath = 'd:\\Temp_D\\Project\\!QuiteRSS\\file'
packerPath = 'd:\\Temp_D\\Project\\!QuiteRSS\\build-updater-Desktop\\release\\target\\7za.exe'
innoSetupCompilerPath = 'c:\\Program Files\\Inno Setup 5\\Compil32.exe'

isTestBuild = 0

# Список файлов состоит из относительного пути папки, содержащей файл,
# и имени файла, который необходимо скопировать
ID_DIR = 0
ID_NAME = 1
filesFromSource = [
    ['\\sound', 'notification.wav'],
    ['\\style', 'gray.qss'],
    ['\\style', 'green.qss'],
    ['\\style', 'orange.qss'],
    ['\\style', 'pink.qss'],
    ['\\style', 'purple.qss'],
    ['\\style', 'system.qss'],
    ['\\style', 'system2.qss'],
    ['\\style', 'news.css'],
    ['', 'AUTHORS'],
    ['', 'COPYING'],
    ['', 'HISTORY_EN'],
    ['', 'HISTORY_RU'],
    ['', 'README']
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
    ['\\phonon_backend', 'phonon_ds94.dll'],
    ['\\codecs', 'qcncodecs4.dll'],
    ['\\codecs', 'qjpcodecs4.dll'],
    ['\\codecs', 'qkrcodecs4.dll'],
    ['\\codecs', 'qtwcodecs4.dll']
]

filesFromQtSDKBin = [
    ['', 'libeay32.dll'],
    ['', 'libgcc_s_dw2-1.dll'],
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

strProductVer = '0.0.0'
strProductRev = '0'
prepareFileList = []


def createPath(path):
    print "---- Preparing path: " + path
    if (os.path.exists(path)):
        print "Path exists. Remove it"
        shutil.rmtree(path)

    os.makedirs(path)
    print "Path created"


def deletePath(path):
    print "---- Deleting path: " + path

    if (os.path.exists(path)):
        print "Path exists. Remove it"
        shutil.rmtree(path)

    print "Path deleted"


def getProductVer():
    print '---- Geting product version'

    global strProductVer

    with open(quiterssSourcePath + '\\src\\VersionNo.h') as f:
        fileLines = f.readlines()
        f.close()

    for line in fileLines:
        l = line.split()
        if len(l) < 3:
            continue
        if l[1] == 'STRPRODUCTVER':
            strProductVer = l[2][1:-3]

    print 'Product version is ' + strProductVer

    print 'Done'


def getProductRev():
    print '---- Geting product revision'
    
    global strProductRev

    with open(quiterssSourcePath + '\\src\\VersionRev.h') as f:
        fileLines = f.readlines()
        f.close()

    for line in fileLines:
        l = line.split()
        if len(l) < 3:
            continue
        if l[1] == 'VCS_REVISION':
            strProductRev = l[2]

    print 'Product revision is ' + strProductRev

    print 'Done'


def makeBin():
    print "---- Making bin..."
    
    curWorkPath = os.getcwd()
    os.chdir(quiterssBuildPath)
       
    # callLine = 'set PATH=' + qtsdkPath + '\\bin'
    # print 'os.system(' + callLine + ')'
    # os.system(callLine)
    
    # callLine = 'set PATH=%PATH%;' + mingwPath + '\\bin'
    # print 'os.system(' + callLine + ')'
    # os.system(callLine)
    
    # callLine = 'set PATH=%PATH%;%SystemRoot%\\System32'
    # print 'os.system(' + callLine + ')'
    # os.system(callLine)
    
    callLine = mingwPath + '\\bin\\mingw32-make clean'
    print 'call(' + callLine + ')'
    call(callLine)
    
    callLine = 'qmake -r -spec win32-g++ CONFIG+=release ' + quiterssSourcePath + "\\QuiteRSS.pro"
    print 'call(' + callLine + ')'
    call(callLine)
    
    callLine = 'mingw32-make'
    print 'call(' + callLine + ')'
    call(callLine)
    
    os.chdir(curWorkPath)

    print "Done"
    

def copyLangFiles():
    print "---- Copying language files..."

    shutil.copytree(quiterssReleasePath + "\\lang", prepareBinPath + "\\lang")
    shutil.copystat(quiterssReleasePath + "\\lang", prepareBinPath + "\\lang")

    global prepareFileList
    langFiles = os.listdir(prepareBinPath + "\\lang")
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
        if file[ID_DIR] and (not os.path.exists(prepareBinPath + file[ID_DIR])):
            os.makedirs(prepareBinPath + file[ID_DIR])

        # Копируем файл, обрабатывая ошибки
        try:
            shutil.copy2(src + file[ID_DIR] + '\\' + file[ID_NAME],
                    prepareBinPath + file[ID_DIR] + '\\' + file[ID_NAME])
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
    shutil.copy2(prepareBinPath + '\\file_list.md5',
            quiterssFileRepoPath + '\\file_list.md5')
    print "Done"


def packFiles(fileList, path):
    '''
    Пакуем каждый файл в индивидуальный архив
    '''
    print '---- Pack files'
    for file in fileList:
        packCmdLine = packerPath \
                + ' a "' + path + file + '.7z" "' + path + file + '"'
        print 'subprocess.call(' + packCmdLine + ')'
        call(packCmdLine)

    print "Done"


def copyPackedFiles():
    print '---- Copying packed files to quiterss.file-repo.windows'

    prepareFileList7z = []
    for file in prepareFileList:
        prepareFileList7z.append(file + '.7z')

    for file in prepareFileList7z:
        print 'copying: ' + file
        shutil.copy2(prepareBinPath + file,
                quiterssFileRepoPath + '\\windows' + file)

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
    global mingwPath
    global quiterssSourcePath
    global quiterssReleasePath
    global updaterPath
    global preparePath
    global prepareBinPath
    global packagesPath
    global testPackagesPath
    global quiterssFileRepoPath
    global packerPath
    global innoSetupCompilerPath

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
    mingwPath = config.get('paths', 'mingwPath')
    quiterssSourcePath = config.get('paths', 'quiterssSourcePath')
    quiterssBuildPath = config.get('paths', 'quiterssBuildPath')
    quiterssReleasePath = quiterssBuildPath + '\\release\\target'
    updaterPath = config.get('paths', 'updaterPath')
    preparePath = config.get('paths', 'preparePath')
    prepareBinPath = preparePath + '\\release'
    packagesPath = config.get('paths', 'packagesPath')
    testPackagesPath = config.get('paths', 'testPackagesPath')
    quiterssFileRepoPath = config.get('paths', 'quiterssFileRepoPath')
    packerPath = config.get('paths', 'packerPath')
    innoSetupCompilerPath = config.get('paths', 'innoSetupCompilerPath')

    print 'Done'


def writeConfigFile():
    configFileName = os.path.basename(sys.argv[0]).replace('.py', '.ini')
    print '---- Writing config file: ' + configFileName

    config = ConfigParser.SafeConfigParser()
    config.optionxform = str
    config.add_section('paths')
    config.set('paths', 'qtsdkPath', qtsdkPath)
    config.set('paths', 'mingwPath', mingwPath)
    config.set('paths', 'quiterssSourcePath', quiterssSourcePath)
    config.set('paths', 'quiterssBuildPath', quiterssBuildPath)
    config.set('paths', 'updaterPath', updaterPath)
    config.set('paths', 'preparePath', preparePath)
    config.set('paths', 'packagesPath', packagesPath)
    config.set('paths', 'testPackagesPath', testPackagesPath)
    config.set('paths', 'quiterssFileRepoPath', quiterssFileRepoPath)
    config.set('paths', 'packerPath', packerPath)
    config.set('paths', 'innoSetupCompilerPath', innoSetupCompilerPath)

    # Writing our configuration to file
    with open(configFileName, 'wb') as configfile:
        config.write(configfile)

    print 'Done'


def makePortableVersion():
    if (isTestBuild != 1):
        path = packagesPath + '\\push\\' + strProductVer
        nameFile = 'QuiteRSS-' + strProductVer
    else:
        path = testPackagesPath
        nameFile = 'QuiteRSS-' + strProductVer + '.' + strProductRev
    tempPath = preparePath + '\\' + nameFile
        
    print '---- Makeing portable version akeing portable version in ' + path
    
    if (os.path.exists(path)):
        print "Path exists. Remove it"
        shutil.rmtree(path, True)

    if (os.path.exists(tempPath)):
        print "Path exists. Remove it"
        shutil.rmtree(tempPath)

    print 'Copying files...'
    shutil.copytree(prepareBinPath, tempPath)
    shutil.copystat(prepareBinPath, tempPath)

    print 'Creating portable.dat...'
    f = open(tempPath + '\\portable.dat', 'w')
    f.close()

    print 'Pack folder...'
    packCmdLine = packerPath + ' a "' + tempPath + '.zip" "' + tempPath + '"'
    print 'subprocess.call(' + packCmdLine + ')'
    call(packCmdLine)
    
    print 'Copying portable package...'
    shutil.copy2(tempPath + '.zip', path + '\\' + nameFile + '.zip')

    print 'Remove temp folder...'
    shutil.rmtree(tempPath)

    print 'Done'


def makeSources():
    sourcesTempPath = packagesPath + '\\' + strProductVer + '\\QuiteRSS-' + strProductVer + '-src'
    print '---- Making sources in ' + sourcesTempPath

    if (os.path.exists(sourcesTempPath)):
        print "Path exists. Remove it"
        shutil.rmtree(sourcesTempPath)

    if (os.path.exists(sourcesTempPath + '.tar.bz2')):
        print "File exists. Remove it"
        os.remove(sourcesTempPath + '.tar.bz2')

    print 'Export mercurial sources...'
    packCmdLine = 'hg archive --cwd ' \
        + quiterssSourcePath + ' --type tbz2 ' + sourcesTempPath + '.tar.bz2'
    print 'subprocess.call(' + packCmdLine + ')'
    call(packCmdLine)

    print 'Done'


def makeInstaller():
    print '---- Making installer...'
    quiterssFileDataPath = quiterssFileRepoPath + '\\installer\\Data'

    if (os.path.exists(quiterssFileDataPath)):
        print "Path ...\\installer\\Data exists. Remove it"
        shutil.rmtree(quiterssFileDataPath)

    print 'Copying files...'
    shutil.copytree(prepareBinPath, quiterssFileDataPath)
    shutil.copystat(prepareBinPath, quiterssFileDataPath)

    print 'Run Inno Setup compiler...'
    cmdLine = [innoSetupCompilerPath,
        '/cc', quiterssFileRepoPath + '\\installer\\quiterss.iss']
    print 'subprocess.call(' + str(cmdLine) + ')'
    call(cmdLine)

    print 'Copying installer...'
    shutil.copy2(quiterssFileRepoPath + '\\installer\\Setup\\QuiteRSS-'
        + strProductVer + '-Setup.exe', packagesPath + '\\' + strProductVer)

    print 'Cleanup installer files...'
    shutil.rmtree(quiterssFileRepoPath + '\\installer\\Data')
    shutil.rmtree(quiterssFileRepoPath + '\\installer\\Setup')

    print 'Done'
    

def createMD5Packages():
    if (isTestBuild != 1):
        path = packagesPath + '\\' + strProductVer
    else:
        path = testPackagesPath
    
    print "---- Create md5-file for packages in " + path
    
    packagesList = []
    
    if (isTestBuild != 1):
        packagesList.append('\\QuiteRSS-' + strProductVer + '.zip')
        packagesList.append('\\QuiteRSS-' + strProductVer + '-Setup.exe')
        packagesList.append('\\QuiteRSS-' + strProductVer + '-src.tar.bz2')
    else:
        packagesList.append('\\QuiteRSS-' + strProductVer + '.' + strProductRev + '.zip')
    
    f = open(path + '\\md5.txt', 'w')
    for file in packagesList:
        fileName = path + file
        fileHash = hashlib.md5(open(fileName, 'rb').read()).hexdigest()
        line = fileHash + ' *' + file[1:]
        f.write(line + '\n')
        print line

    f.close()
    
    print 'Done'
    

def finalize():
    print
    print '  ###    ###   #   #  #####      #  #  #  '
    print '  #  #  #   #  ##  #  #          #  #  #  '
    print '  #  #  #   #  # # #  ####       #  #  #  '
    print '  #  #  #   #  #  ##  #                   '
    print '  ###    ###   #   #  #####      #  #  #  '
    print


def main():
    print "QuiteRSS prepare-install"
    global isTestBuild
    
    if (sys.argv[1] == '--build-test'):
        isTestBuild = 1
        print 'Build test version'
    
    readConfigFile()
    createPath(prepareBinPath)
    makeBin()
    getProductVer()
    getProductRev()
    copyLangFiles()
    copyFileList(filesFromRelease, quiterssReleasePath)
    copyFileList(filesFromUpdater, updaterPath)
    copyFileList(filesFromSource, quiterssSourcePath)
    copyFileList(filesFromQtSDKPlugins, qtsdkPath + '\\plugins')
    copyFileList(filesFromQtSDKBin, qtsdkPath + '\\bin')
    makePortableVersion()
    if (isTestBuild != 1):
        makeSources()
        makeInstaller()
        createMD5(prepareFileList, preparePath)
        copyMD5()
        packFiles(prepareFileList, preparePath)
        copyPackedFiles()
        if (len(sys.argv) < 2) or (sys.argv[1] != '--dry-run'):
            updateFileRepo()
    createMD5Packages()
        
    deletePath(preparePath)
    writeConfigFile()
    finalize()


if __name__ == '__main__':
    main()
