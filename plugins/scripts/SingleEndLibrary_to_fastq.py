#!/usr/bin/env python

# standard library imports
import os
import sys
import traceback
import argparse
import json
import logging
import hashlib

# 3rd party imports
import requests

# KBase imports
import biokbase.RNASeq.script_util as script_utils
import biokbase.workspace.client


# conversion method that can be called if this module is imported
def convert(workspace_service_url, shock_service_url, handle_service_url, workspace_name, object_name,object_type, working_directory, level=logging.INFO, logger=None):

    """
    Converts KBaseAssembly.SingleEndLibrary to a Fasta file of assembledDNA.

    Args:
	workspace_service_url :  A url for the KBase Workspace service
        shock_service_url: A url for the KBase SHOCK service.
        handle_service_url: A url for the KBase Handle Service.
        workspace_name : Name of the workspace
        object_name : Name of the object in the workspace
        working_directory : The working directory for where the output file should be stored.
        level: Logging level, defaults to logging.INFO.

    """

    if not os.path.isdir(args.working_directory):
        raise Exception("The working directory does not exist {0} does not exist".format(working_directory))

    md5 = None 
    if logger is None:
        logger = script_utils.stderrLogger(__file__)
    
    logger.info("Starting conversion of KBaseAssembly.SingleEndLibrary to FASTA.")

    token = os.environ.get('KB_AUTH_TOKEN')
    
    logger.info("Gathering information.")
    try:
   	 ws_client = biokbase.workspace.client.Workspace('https://ci.kbase.us/services/ws')
    except Exception,e:
	raise Exception("Could not create workspace client")
    if object_type in ("SingleEnd"):
	print "entering if" 
    	single_end_library = ws_client.get_objects([{'workspace':workspace_name,'name':object_name}])[0]['data'] 

    	shock_id = None
    	if "handle" in single_end_library and "id" in single_end_library['handle']:
		shock_id  = single_end_library['handle']['id']
		print shock_id
    	if shock_id is None:
        	raise Exception("There was not shock id found.")
	try:
                script_utils.download_file_from_shock(logger, shock_service_url, shock_id, working_directory, token)
	except Exception,e:
		print e
	        raise Exception( "Unable to download shock file , {0}".format(e))
	
	logger.info("Conversion completed.")
    elif object_type in ("PairedEnd"):
	paired_end_library = ws_client.get_objects([{'workspace':workspace_name,'name':object_name}])[0]['data']
	shock_id1 = None
	shock_id2 = None
        if "handle_1" in paired_end_library and "id" in paired_end_library['handle']:
                shock_id1  = paired_end_library['handle_1']['id']
        if shock_id1 is None:
                raise Exception("Handle1 there was not shock id found.")
	if "handle_2" in paired_end_library and "id" in paired_end_library['handle']:
                shock_id2  = paired_end_library['handle_2']['id']
        if shock_id2 is None:
                raise Exception("Handle2 there was not shock id found.")
	
        script_utils.download_file_from_shock(logger, shock_service_url, shock_id1, working_directory, token)
        script_utils.download_file_from_shock(logger, shock_service_url, shock_id2, working_directory, token)
        logger.info("Conversion completed.")
#    if "handle" in ws_object and  "remote_md5" in single_end_library['handle']:
#	md5 = single_end_library['handle']['remote_md5']    	
    


# called only if script is run from command line
if __name__ == "__main__":	
    parser = argparse.ArgumentParser(prog='trns_transform_KBaseAssembly.SingleEndLibrary-to-KBaseAssembly.FA', 
                                     description='Converts SingleEndLibrary file to fasta file',
                                     epilog='Authors: Srividya Ramakrishnan, Matt Henderson, Jason Baumohl')
    parser.add_argument('--workspace_service_url', help='Workspace service url', action='store', type=str, nargs='?', required=True)
    parser.add_argument('--workspace_name', help ='Workspace Name', action='store', type=str, nargs='?', required=True)
    parser.add_argument('--working_directory', help ='Directory the output file(s) should be written into', action='store', type=str, nargs='?', required=True)

    object_info = parser.add_mutually_exclusive_group(required=True)
    object_info.add_argument('--object_name', help ='Object Name', action='store', type=str, nargs='?')
    object_info.add_argument('--object_id', help ='Object ID', action='store', type=str, nargs='?')
    parser.add_argument('--object_type', help='Object type', action='store', type=str, nargs='?',required=True)
#NOTE VERSION NUMBER NEEDS TO BE ADDED

    data_services = parser.add_mutually_exclusive_group(required=True)
    data_services.add_argument('--shock_service_url', help='Shock url', action='store', type=str, default='https://kbase.us/services/shock-api/', nargs='?')
    data_services.add_argument('--handle_service_url', help='Handle service url', action='store', type=str, default='https://kbase.us/services/handle_service/', nargs='?') 


    args = parser.parse_args()

    logger = script_utils.stderrlogger(__file__)

    try:
        convert(args.workspace_service_url,args.shock_service_url, args.handle_service_url,args.workspace_name,args.object_name, args.object_type,args.working_directory, logger=logger) 

    except:
        logger.exception("".join(traceback.format_exc()))
        sys.exit(1)
    
    sys.exit(0)

