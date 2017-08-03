# revit-3d-print

## Requirements

- Windows v7, v10
- Autodesk Revit v2016, v2017
- [Dynamo](http://dynamobim.org/download/) v1.2.x, v1.3.x

## Installing

- [Git](https://git-scm.com/download/win)
- Python
	- [Python](https://www.python.org/downloads/)  v2.7.x
	- [Pillow](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow) v3.4.2
- .svx to .stl (Java)
	- [code](https://github.com/AbFab3D/AbFab3D), [post](https://abfab3d.com/svx-format/)
	- [JDK](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) v8
	- [Apache Ant](http://ant.apache.org/bindownload.cgi)
- setup Environment Variables: adjust the directory based on your downloaded location/version
	- `JAVA_HOME`: `C:\Program Files\Java\jdk1.8.0_101`
	- `ANT_HOME`: `C:\Program Files\apache-ant-1.9.7`
	- `PATH`: append to the end
		- `C:\Python27`
		- `C:\Python27\Scripts`
		- `%ANT_HOME%\bin`

## Layout

	/archive                 ... archive Dynamo scripts
	/script                  ... python script
	/image                   ... empty output folder
		/origin              ... original Section View .png images
		/invert              ... invert .png images 
		manifest.xml         ... .svx configuration
		model.svx            ... .svx model
	README.md                
	dynamicSectionView.dyn   ... main Dynamo script

## How to

- create View Template in Revit
- setup parameters in `dynamicSectionView.dyn`
- create `image` folder
- run `dynamicSectionView.dyn`
- get `model.svx`

## Team
* [Yueying Cui][1]
* [Chris Winkler][2]
* Youngjin Lee
* Ken Goulding

## Reference

[1]: mailto:ycui@sasaki.com
[2]: mailto:cwinkler@sasaki.com
