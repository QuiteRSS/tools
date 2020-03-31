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

qtsdkPath = 'C:\\Qt\\5.14.1\\msvc2017'
opensslPath = 'c:\\Program Files (x86)\\OpenSSL-Win32'
quiterssSourcePath = 'd:\\Programming\\QuiteRSS\\quiterss'
quiterssBuildPath = 'd:\\Programming\\QuiteRSS\\build-QuiteRSS-Desktop'
updaterPath = 'd:\\Programming\\QuiteRSS\\build-updater-Desktop\\release\\target'
preparePath = 'd:\\Programming\\QuiteRSS\\prepare-install-build'
packagesPath = 'd:\\Programming\\Version\\push'
testPackagesPath = 'd:\\Programming\\YandexDisk\\QuiteRSS-test'
quiterssToolsPath = 'd:\\Programming\\QuiteRSS\\tools'
packerPath = 'd:\\Programming\\QuiteRSS\\build-updater-Desktop\\release\\target\\7za.exe'
innoSetupCompilerPath = 'c:\\Program Files (x86)\\Inno Setup 5\\Compil32.exe'
vcredistPath = 'c:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\VC\\Redist\\MSVC\\14.16.27012\\x86\\Microsoft.VC141.CRT'

quiterssReleasePath = ''
prepareBinPath = ''

serverFtp = 'server.org'
userFtp = 'user'
passFtp = 'pass'

operationType = 0

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
    ['\\style', 'Rstyle_v1.2.css'],
    ['\\style', 'dark.qss'],
    ['\\style', 'web_dark.css'],
    ['', 'AUTHORS'],
    ['', 'COPYING'],
    ['', 'HISTORY_EN'],
    ['', 'HISTORY_RU'],
    ['', 'README.md']
]

filesFromRelease = [
    ['', 'QuiteRSS.exe']
]

filesFromUpdater = [
    ['', '7za.exe'],
    ['', 'Updater.exe']
]

filesFromQtSDKPlugins = [
    ['\\audio', 'qtaudio_wasapi.dll'],
    ['\\audio', 'qtaudio_windows.dll'],
    ['\\bearer', 'qgenericbearer.dll'],
    ['\\iconengines', 'qsvgicon.dll'],
    ['\\imageformats', 'qgif.dll'],
    ['\\imageformats', 'qicns.dll'],
    ['\\imageformats', 'qico.dll'],
    ['\\imageformats', 'qjpeg.dll'],
    ['\\imageformats', 'qsvg.dll'],
    ['\\imageformats', 'qtga.dll'],
    ['\\imageformats', 'qtiff.dll'],
    ['\\imageformats', 'qwbmp.dll'],
    ['\\imageformats', 'qwebp.dll'],
    ['\\mediaservice', 'dsengine.dll'],
    ['\\mediaservice', 'qtmedia_audioengine.dll'],
    ['\\mediaservice', 'wmfengine.dll'],
    ['\\platforms', 'qwindows.dll'],
    ['\\printsupport', 'windowsprintersupport.dll'],
    ['\\sqldrivers', 'qsqlite.dll'],
    ['\\styles', 'qwindowsvistastyle.dll']
]

filesFromQtSDKBin = [
    ['', 'icudt65.dll'],
    ['', 'icuin65.dll'],
    ['', 'icuuc65.dll'],
    ['', 'libxml2.dll'],
    ['', 'libxslt.dll'], 
    ['', 'Qt5Core.dll'],
    ['', 'Qt5Gui.dll'],
    ['', 'Qt5Multimedia.dll'],
    ['', 'Qt5Network.dll'],
    ['', 'Qt5Positioning.dll'],
    ['', 'Qt5PrintSupport.dll'],
    ['', 'Qt5Qml.dll'],
    ['', 'Qt5QmlModels.dll'],
    ['', 'Qt5Quick.dll'],
    ['', 'Qt5Sensors.dll'],
    ['', 'Qt5Sql.dll'],
    ['', 'Qt5Svg.dll'],
    ['', 'Qt5WebChannel.dll'],
    ['', 'Qt5WebKit.dll'],
    ['', 'Qt5WebKitWidgets.dll'],
    ['', 'Qt5Widgets.dll'],
    ['', 'Qt5Xml.dll']
]

filesFromOpenSSL = [
    ['', 'libcrypto-1_1.dll'],
    ['', 'libssl-1_1.dll']
]

filesFromVcredist = [
    ['', 'msvcp140.dll'],
    ['', 'vcruntime140.dll']
]

strProductVer = '0.0.0'
strProductRev = '0'
prepareFileList = []


def createPath(path, ignore_errors=False):
    print "---- Creating path: " + path
    if (os.path.exists(path)):
        print "Path exists. Remove it"
        shutil.rmtree(path, ignore_errors)

    if (not os.path.exists(path)):
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
    
    callLine = 'jom clean'
    print 'call(' + callLine + ')'
    call(callLine)
    
    callLine = 'qmake -spec win32-msvc CONFIG+=release ' + quiterssSourcePath + '\\QuiteRSS.pro'
    print 'call(' + callLine + ')'
    call(callLine)

    callLine = 'jom qmake_all'
    print 'call(' + callLine + ')'
    call(callLine)
    
    callLine = 'jom -j3'
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


def readConfigFile():
    global qtsdkPath
    global opensslPath
    global quiterssSourcePath
    global quiterssBuildPath
    global quiterssReleasePath
    global updaterPath
    global preparePath
    global prepareBinPath
    global packagesPath
    global testPackagesPath
    global quiterssToolsPath
    global packerPath
    global innoSetupCompilerPath
    global vcredistPath
    
    global serverFtp
    global userFtp
    global passFtp

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
    opensslPath = config.get('paths', 'opensslPath')
    quiterssSourcePath = config.get('paths', 'quiterssSourcePath')
    quiterssBuildPath = config.get('paths', 'quiterssBuildPath')
    quiterssReleasePath = quiterssBuildPath + '\\release\\target'
    updaterPath = config.get('paths', 'updaterPath')
    preparePath = config.get('paths', 'preparePath')
    prepareBinPath = preparePath + '\\release'
    packagesPath = config.get('paths', 'packagesPath')
    testPackagesPath = config.get('paths', 'testPackagesPath')
    quiterssToolsPath = config.get('paths', 'quiterssToolsPath')
    packerPath = config.get('paths', 'packerPath')
    innoSetupCompilerPath = config.get('paths', 'innoSetupCompilerPath')
    vcredistPath = config.get('paths', 'vcredistPath')
      
    serverFtp = config.get('ftp', 'serverFtp')
    userFtp = config.get('ftp', 'userFtp')
    passFtp = config.get('ftp', 'passFtp')

    print 'Done'


def writeConfigFile():
    configFileName = os.path.basename(sys.argv[0]).replace('.py', '.ini')
    print '---- Writing config file: ' + configFileName

    config = ConfigParser.SafeConfigParser()
    config.optionxform = str
    config.add_section('paths')
    config.set('paths', 'qtsdkPath', qtsdkPath)
    config.set('paths', 'opensslPath', opensslPath)
    config.set('paths', 'quiterssSourcePath', quiterssSourcePath)
    config.set('paths', 'quiterssBuildPath', quiterssBuildPath)
    config.set('paths', 'updaterPath', updaterPath)
    config.set('paths', 'preparePath', preparePath)
    config.set('paths', 'packagesPath', packagesPath)
    config.set('paths', 'testPackagesPath', testPackagesPath)
    config.set('paths', 'quiterssToolsPath', quiterssToolsPath)
    config.set('paths', 'packerPath', packerPath)
    config.set('paths', 'innoSetupCompilerPath', innoSetupCompilerPath)
    config.set('paths', 'vcredistPath', vcredistPath)

    # Writing our configuration to file
    with open(configFileName, 'wb') as configfile:
        config.write(configfile)

    print 'Done'


def makePortableVersion():
    if (operationType != 1):
        nameFile = 'QuiteRSS-' + strProductVer
    else:
        nameFile = 'QuiteRSS-' + strProductVer + '.' + strProductRev
    tempPath = preparePath + '\\' + nameFile
        
    print '---- Makeing portable version akeing portable version in ' + packagesPath
    
    createPath(packagesPath, True)
    deletePath(tempPath)

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
    shutil.copy2(tempPath + '.zip', packagesPath + '\\' + nameFile + '.zip')

    print 'Remove temp folder...'
    shutil.rmtree(tempPath)

    print 'Done'


def makeSources():
    sourcesTempPath = packagesPath + '\\QuiteRSS-' + strProductVer + '-src'
    print '---- Making sources in ' + sourcesTempPath

    if (os.path.exists(sourcesTempPath)):
        print "Path exists. Remove it"
        shutil.rmtree(sourcesTempPath)

    if (os.path.exists(sourcesTempPath + '.tar.gz')):
        print "File exists. Remove it"
        os.remove(sourcesTempPath + '.tar.gz')

    print 'Export git sources...'
    packCmdLine = 'git archive master --remote="' \
        + quiterssSourcePath + '" | gzip > "' + sourcesTempPath + '.tar.gz"'
    print 'subprocess.call(' + packCmdLine + ')'
    os.system(packCmdLine)

    print 'Done'


def makeInstaller():
    print '---- Making installer...'
    quiterssFileDataPath = quiterssToolsPath + '\\installer\\Data'

    if (os.path.exists(quiterssFileDataPath)):
        print "Path ...\\installer\\Data exists. Remove it"
        shutil.rmtree(quiterssFileDataPath)

    print 'Copying files...'
    shutil.copytree(prepareBinPath, quiterssFileDataPath)
    shutil.copystat(prepareBinPath, quiterssFileDataPath)

    print 'Run Inno Setup compiler...'
    cmdLine = [innoSetupCompilerPath,
        '/cc', quiterssToolsPath + '\\installer\\quiterss.iss']
    print 'subprocess.call(' + str(cmdLine) + ')'
    call(cmdLine)

    print 'Copying installer...'
    shutil.copy2(quiterssToolsPath + '\\installer\\Setup\\QuiteRSS-'
        + strProductVer + '-Setup.exe', packagesPath)

    print 'Cleanup installer files...'
    shutil.rmtree(quiterssToolsPath + '\\installer\\Data')
    shutil.rmtree(quiterssToolsPath + '\\installer\\Setup')

    print 'Done'
    

def createMD5Packages():
    print "---- Create md5-file for packages in " + packagesPath
    packagesMd5File = packagesPath + '\\QuiteRSS-' + strProductVer + '.md5'
        
    if (os.path.exists(packagesMd5File)):
        os.remove(packagesMd5File)
    
    filesList = os.listdir(packagesPath)
    f = open(packagesMd5File, 'w')
    for fileName in filesList:
        fileHash = hashlib.md5(open(packagesPath + '\\' + fileName, 'rb').read()).hexdigest()
        line = fileHash + ' *' + fileName
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
    
    
def sendUpdateFilesFtp():
    print "---- Send update files by FTP"
    global serverFtp
    global userFtp
    global passFtp
    
    from ftplib import FTP_TLS
    ftps = FTP_TLS(serverFtp)
    ftps.set_debuglevel(1)
    ftps.login(userFtp, passFtp)
    ftps.prot_p()
    ftps.cwd('/files/updates_new')
    
    ftps.storbinary('STOR ' + 'file_list.md5', open(prepareBinPath + '\\file_list.md5', 'rb'))
    ftps.storbinary('STOR ' + 'VersionNo.h', open(quiterssSourcePath + '\\src\\VersionNo.h', 'rb'))
    ftps.storbinary('STOR ' + 'HISTORY_EN', open(quiterssSourcePath + '\\HISTORY_EN', 'rb'))
    ftps.storbinary('STOR ' + 'HISTORY_RU', open(quiterssSourcePath + '\\HISTORY_RU', 'rb'))
    
    prepareFileList7z = []
    for file in prepareFileList:
        prepareFileList7z.append(file + '.7z')

    for fileName in prepareFileList7z:
        ftps.storbinary('STOR ' + 'windows' + fileName.replace('\\','/'), open(prepareBinPath + fileName, 'rb'))

    ftps.quit()

    
def sendPackagesFtp():
    print "---- Send packages by FTP"
    global serverFtp
    global userFtp
    global passFtp
    packagesMd5File = packagesPath + '\\QuiteRSS-' + strProductVer + '.md5'

    from ftplib import FTP_TLS
    ftps = FTP_TLS(serverFtp)
    ftps.set_debuglevel(1)
    ftps.login(userFtp, passFtp)
    ftps.prot_p()
    try:
        ftps.sendcmd('MKD ' + '/files/' + strProductVer)
    except Exception:
        print 'Directory already exists'
    ftps.cwd('/files/' + strProductVer)
    
    filesListFtp = ftps.nlst()
    filesList = os.listdir(packagesPath)
    newFilesList = [e for e in filesList if not(e in filesListFtp)]
    
    ftps.storbinary('STOR ' + 'QuiteRSS-' + strProductVer + '.md5', open(packagesMd5File, 'rb'))
    for fileName in newFilesList:
        ftps.storbinary('STOR ' + fileName, open(packagesPath + '\\' + fileName, 'rb'))

    ftps.quit()


def main():
    print "---- QuiteRSS prepare-install"
    global operationType
    global packagesPath
    
    if (len(sys.argv) > 1) and (sys.argv[1] == '--build-test'):
        operationType = 1
        print 'Operation type: Build test version'
    elif (len(sys.argv) > 1) and (sys.argv[1] == '--send-files'):
        operationType = 2
        print 'Operation type: Only sending files by FTP'
    else:
        print 'Operation type: Build all packages'
    
    readConfigFile()
    
    if (operationType != 2):
        createPath(prepareBinPath)
        makeBin()
    
    getProductVer()
    getProductRev()
    
    if (operationType != 1):
        packagesPath = packagesPath + '\\' + strProductVer
    else:
        packagesPath = testPackagesPath
        
    if (operationType != 2):
        copyLangFiles()
        copyFileList(filesFromRelease, quiterssReleasePath)
        copyFileList(filesFromUpdater, updaterPath)
        copyFileList(filesFromSource, quiterssSourcePath)
        copyFileList(filesFromQtSDKPlugins, qtsdkPath + '\\plugins')
        copyFileList(filesFromQtSDKBin, qtsdkPath + '\\bin')
        copyFileList(filesFromOpenSSL, opensslPath + '\\bin')
        copyFileList(filesFromVcredist, vcredistPath)
        makePortableVersion()
        
        if (operationType != 1):
            makeSources()
            makeInstaller()
            createMD5(prepareFileList, prepareBinPath)
            packFiles(prepareFileList, prepareBinPath)
            if (len(sys.argv) < 2) or (sys.argv[1] != '--dry-run'):
                sendUpdateFilesFtp()
                
        deletePath(preparePath)
        
    createMD5Packages()
    
    if (operationType != 1):
        sendPackagesFtp()
        
    finalize()


if __name__ == '__main__':
    main()
