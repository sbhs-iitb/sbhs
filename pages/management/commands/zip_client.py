from django.core.management.base import BaseCommand
import os, zipfile, shutil, distutils.core
from sbhs_server import settings

class Command(BaseCommand):
    args = ''
    help = 'ZIP all clients for all architectures.'

    def handle(self, *args, **options):
        def zipdir(path, zip, rootname):
            for root, dirs, files in os.walk(path):
                for file in files:
                    pathname = os.path.join(root, file)
                    zip.write(pathname, rootname + "/" + pathname.replace(path, ""))

        scilab_codes_dirname = "scilab_codes"
        scilab_codes_dirpath = os.path.join(settings.SBHSCLIENT_STATIC_DIR, scilab_codes_dirname)
        zipped_dirname = "zipped"
        zipped_dirpath = os.path.join(settings.SBHSCLIENT_STATIC_DIR, zipped_dirname)

        dirs = os.listdir(settings.SBHSCLIENT_STATIC_DIR)
        print dirs
        dirs.remove(scilab_codes_dirname)
        dirs.remove(zipped_dirname)
	print dirs
        dirs = [d for d in dirs if os.path.isdir(os.path.join(settings.SBHSCLIENT_STATIC_DIR, d))]
        print dirs
        dirs = [d for d in dirs if not d.startswith(".")]

        for dirname in dirs:
            print dirname
            dirpath = os.path.join(settings.SBHSCLIENT_STATIC_DIR, dirname)
            tmp_dirpath = os.path.join(zipped_dirpath, dirname)
            common_files_dirpath = os.path.join(dirpath, "common_files")
            run_file_dirpath = os.path.join(dirpath, "run_file")

            os.mkdir(tmp_dirpath)
            for f in os.listdir(dirpath):
                if os.path.isfile(os.path.join(dirpath, f)):            
                    shutil.copy(os.path.join(dirpath, f), os.path.join(tmp_dirpath, f))

            if dirname not in ["analysis", "local"]:
                distutils.dir_util.copy_tree(scilab_codes_dirpath, tmp_dirpath)
            else:
                distutils.dir_util.copy_tree(dirpath, tmp_dirpath)
            try:
                shutil.rmtree(tmp_dirpath + "/" + scilab_codes_dirname + "/.git")
            except:
                pass
    
            try:
                for root, dirs, files in os.walk(tmp_dirpath):
                    if os.path.exists(os.path.join(root, "scilabread.sce")):
                        distutils.dir_util.copy_tree(run_file_dirpath, root)
            except:
                pass
    
            try:
                distutils.dir_util.copy_tree(common_files_dirpath, os.path.join(tmp_dirpath, "common_files"))
            except:
                pass
    
            zipf = zipfile.ZipFile(os.path.join(zipped_dirpath, "sbhsclient/scilab_codes_" + dirname + ".zip"), 'w', zipfile.ZIP_DEFLATED)
            zipdir(tmp_dirpath, zipf, "scilab_codes_" + dirname)
            zipf.close()
            shutil.rmtree(tmp_dirpath)
