#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# PKG PATCHER 1.0 by drchannn
#
#############################

import sys
import os
import shutil
import subprocess

from datetime import datetime

#APP_PATH=os.path.dirname(os.path.abspath(__file__))
APP_PATH=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])))

def __l(mensaje, noprint=0):
	salida = '>> %s | [%s] '  % (datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), mensaje)
	if (noprint==0): print (salida)
	else: return salida




# GET FILE FOLDER
def get_file_folder(carpeta):
	resultado = "error"
	fichero=os.listdir(carpeta)
	if (len(fichero)==1): resultado = fichero[0]
	return resultado

# GET INFO PKG
def get_info_pkg(fichero):
	title_id="error"
	version="error"
	orbiscmd_exe = "%s\\tools\\orbis\\orbis-pub-cmd.exe" % (APP_PATH)
	orbis_info_cmd=[orbiscmd_exe,"img_info",fichero]
	sp = subprocess.run(orbis_info_cmd, capture_output=True, text=True, shell=True)
	for k in sp.stdout.strip().split("\n"):
		if (k.find("Title ID:")==0): title_id = k[10:]
		if (k.find("Application Version(APP_VER):")==0): version = k[30:]
	return title_id,version

# EXTRACT PKG
def extract_update(patch_pkg, title_id):
	orbiscmd_exe = "%s\\tools\\orbis\\orbis-pub-cmd.exe" % (APP_PATH)
	orbis_extract_cmd=[orbiscmd_exe,"img_extract","--passcode","00000000000000000000000000000000",patch_pkg,APP_PATH+"\\tmp"]
	sp = subprocess.run(orbis_extract_cmd, capture_output=True, text=True, shell=False)
	shutil.copytree(APP_PATH+"\\tmp\\Sc0", APP_PATH+"\\tmp\\Image0\\sce_sys", dirs_exist_ok=True)
	shutil.rmtree(APP_PATH+"\\tmp\\Sc0")
	os.rename(APP_PATH+"\\tmp\\Image0", APP_PATH+"\\tmp\\"+title_id+"-patch")

# CREATE GP4
def create_gp4(patch_extracted, game_pkg):
	gengp4_exe = "%s\\tools\\orbis\\gengp4_patch.exe" % (APP_PATH)
	gengp4_patch_cmd=[gengp4_exe,patch_extracted]
	sp = subprocess.run(gengp4_patch_cmd, capture_output=True, text=True, shell=False)
	orbiscmd_exe = "%s\\tools\\orbis\\orbis-pub-cmd.exe" % (APP_PATH)
	orbis_patchgp4_cmd=[orbiscmd_exe,"gp4_proj_update","--app_path",game_pkg,patch_extracted+".gp4"]
	sp = subprocess.run(orbis_patchgp4_cmd, capture_output=True, text=True, shell=False)

# CREATE PKG
def create_pkg(gp4_file, title_id):
	orbiscmd_exe = "%s\\tools\\orbis\\orbis-pub-cmd.exe" % (APP_PATH)
	orbis_createpkg_cmd=[orbiscmd_exe,"img_create",gp4_file,APP_PATH+"\\"+title_id+"-MOD.pkg"]
	sp = subprocess.run(orbis_createpkg_cmd, capture_output=True, text=True, shell=False)



#### MAIN ######
if __name__ == '__main__':
	os.system('cls')
	__l("START PKG PATCHER")
	
	__l("CHECKING GAME PKG")
	game_pkg=get_file_folder(APP_PATH+"\\game")
	if(game_pkg=="error"):
		input(__l("MISSING PKG ON GAME FOLDER] - Press a key to continue . . .",1))
		exit()
	game_id=get_info_pkg(APP_PATH+"\\game\\"+game_pkg)[0]
	if(game_id=="error"):
		input(__l("ERROR CHECKING GAME PKG] - Press a key to continue . . .",1))
		exit()
	
	__l("CHECKING PATCH PKG")
	patch_pkg=get_file_folder(APP_PATH+"\\patch")
	if(patch_pkg=="error"):
		input(__l("MISSING PKG ON PATCH FOLDER] - Press a key to continue . . .",1))
		exit()

	patch_id,patch_version = get_info_pkg(APP_PATH+"\\patch\\"+patch_pkg)
	if(patch_pkg=="error"):
		input(__l("ERROR CHECKING PATCH PKK] - Press a key to continue . . .",1))
		exit

	if(game_id!=patch_id): 
		input(__l("TITLE ID MISMATCH GAME PATCH] - Press a key to continue . . .",1))
		exit()
	title_id=game_id
	
	__l("EXTRACTING PATCH PKG")
	if(os.path.isdir(APP_PATH+"\\tmp\\"+title_id+"-patch")==False): extract_update(APP_PATH+"\\patch\\"+patch_pkg,title_id)
	if(os.path.isfile(APP_PATH+"\\tmp\\"+title_id+"-patch\\sce_sys\\param.sfo")==False):
		input(__l("ERROR IN EXTRACTED FILES] - Press a key to continue . . .",1))
		exit()
		
	__l("COPYING NEW FILES")
	shutil.copytree(APP_PATH+"\\modz", APP_PATH+"\\tmp\\"+title_id+"-patch", dirs_exist_ok=True)
	
	__l("CREATING GP4")
	create_gp4(APP_PATH+"\\tmp\\"+title_id+"-patch", APP_PATH+"\\game\\"+game_pkg)
	__l("CREATING NEW PKG")
	create_pkg(APP_PATH+"\\tmp\\"+title_id+"-patch.gp4", title_id)
	
	input(__l("FINISH START PKG PATCHER",1))
	exit()
	

