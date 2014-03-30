# Script to generate the zip files required for <datadir zip="true"> in the
# addon.xml of a repository

import os
import xml.etree.ElementTree
from zipfile import ZipFile

def get_plugin_version(addon_dir):
  addon_file = os.path.join(addon_dir, 'addon.xml') 
  try:
    data = open(addon_file, 'r').read()
    node = xml.etree.ElementTree.XML(data)
    return(node.get('version'))
  except Exception as e:
    print 'Failed to open %s' % addon_file
    print e.message


def create_zip_file(addon_dir):
  version = get_plugin_version(addon_dir)
  if not version:
    return
  if not os.path.exists(".." + os.sep + "packages-generated" + os.sep + addon_dir):
        os.makedirs(".." + os.sep + "packages-generated" + os.sep + addon_dir)
  with ZipFile(".." + os.sep + "packages-generated" + os.sep + addon_dir + os.sep + addon_dir + '-' + version + '.zip',
               'w') as addonzip:
    for root, dirs, files in os.walk(addon_dir):
      for file_path in files:
        if file_path.endswith('.zip') or file_path.startswith('.git'):
          continue
        print "adding %s" % os.path.join(root, file_path) 
        # if dirs:
        #   arcname = os.path.join(addon_dir, os.path.join(*dirs), file_path)
        # else:
        #   arcname = os.path.join(addon_dir, file_path)
        # print arcname
        addonzip.write(os.path.join(root, file_path))
    addonzip.close()


def main():
  os.chdir('source')
  dirs = (os.listdir('.'))
  for addon_dir in dirs:
    if(not os.path.isdir(addon_dir)):
      continue	  
    if(addon_dir.startswith('.')):
      # skip hidden dirs
      continue
    if(addon_dir.startswith('tools')):
      # skip hidden dirs
      continue
    create_zip_file(addon_dir)

if __name__ == '__main__':
  main()
