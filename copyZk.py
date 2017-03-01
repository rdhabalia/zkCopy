#!/bin/bash

from kazoo.client import KazooClient
import sys
import json
import argparse
import ConfigParser
import os

def traverse(srcZk, parent, children, targetZk, targetParent, dryRun):
	for child in children:
		targetChild = targetParent + "/"+ child
		child = parent + "/"+ child
		print ("child= "+child+", targetChild= "+targetChild)
		try:
			data = srcZk.get(child)[0]
			if (targetZk.exists(targetChild, None) is not None):
				if not (dryRun):
					targetZk.set(targetChild, data, -1)
				else:
					print ("DRY-RUN set data on ="+targetChild)	
			else:
				if not (dryRun):
					targetZk.create(targetChild, data, None, False, False, True)
				else:
					print ("DRY-RUN create path ="+targetChild)	
			print data
		except Exception as e:
			print ("No data for zk-node " + child + ", exception = " + repr(e))

		try :
			nextChildren = srcZk.get_children(child)
			if nextChildren:
				traverse(srcZk,child,nextChildren,targetZk,targetChild,dryRun)
			else:
				print ("completed zk-copy " + child)
		except Exception as e:
			print ("No children for zk-node "+ child + ", exception = " + repr(e))
		
def main(args):
		sourceZkPath = args.sourceZkPath
		targetZkPath = args.targetZkPath
		dryRun =  args.dry_run
		srcString = sourceZkPath.split("#");
		trgString = targetZkPath.split("#");
		srcZkStr = srcString[0]
		srcZkPath = srcString[1]
		trgZkStr = trgString[0]
		trgZkPath = trgString[1]
		result = not (dryRun)
		print result
		print (srcZkStr + "," + srcZkPath)

		# traverse all children of path
		srcZk = KazooClient(hosts=srcZkStr)
		srcZk.start()
		targetZk = KazooClient(hosts=trgZkStr)
		targetZk.start()
		children = srcZk.get_children(srcZkPath)
		traverse(srcZk, srcZkPath, children, targetZk, trgZkPath, dryRun)


if __name__ in '__main__':
		parser = argparse.ArgumentParser()
		parser.add_argument("--dry-run", "-r", action='store_true', default=False, help="Only prints update cluster data, does not update the zk")
		parser.add_argument("--sourceZkPath", "-szkp", required=True, help="Source ZooKeeperServer:port:path")
		parser.add_argument("--targetZkPath", "-tzkp", required=True, help="Target ZooKeeperServer:port:path")
		args = parser.parse_args()
		main(args)