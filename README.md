# zkCopy
Tool for fast copying ZooKeeper data between different clusters.


## Requirements

- Python
- [kazoo](http://kazoo.readthedocs.io/en/latest/install.html)


## Usage
```
 --dry-run <true|false>                     (optional) set this flag if you just want 
                                to do dry-run without copying and debug logs
               
 -szkp,--sourceZkPath <server:port#path>   location of a source tree to copy
 -tzkp,--targetZkPath <server:port#path>   target location

```