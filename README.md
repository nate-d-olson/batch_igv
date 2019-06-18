# batch_igv
Automating image generation in IGV by generating batch script.

The script uses external packages, therefore, before attempting to use the script one needs to verify that the following libraries are installed:

1. Pandas
2. ArgParse
3. os
4. sys
5. time

positional arguments:

1. igvSession   Name of IGV Session
2. windowSize   Size of Window
3. batchFile    Batch File Name
4. snapshotDir  Snapshots Directory
5. variantPos   Variant Positions
6. pathToIGV    Path to IGV batch

optional arguments:  

`-h`, `--help`   show this help message and exit  
`--runScript`  Choice to run script in IGV automatically (Optional) . 

The very first argument specifies the igv session that is being used for analysis, when specifying the name of session include the path to it.
The second argument specifies the window size, which controls how many reads you will be able to see for each track. This also influences the size of the images.
The third argument is the name under which you would like to save the generated batch script.
The fourth argument designates the snapshot directory, which is the location where the images will be saved to.
The fifth arguement is the file with the variant positions/locations where the snapshots need to be taken (should preferably be a .csv file to guarantee that the script runs),
which also needs to be expressed as a path and name.
Finally, the sixth argument is the path to the IGV batch, which is a crucial component if batch script needs to be run automatically. Also needs to be expressed as path.

Listed above are the six mandatory arguments, however, there is a seventh optional argument (`--runScript`) which needs to be included if you would like to automatically generate 
the snapshots using the generated batch script to be run automatically.

Down below are examples of how you would call the script in a command line:

Example w/o optional parameter:  
```
python batch_igv.py C:\Users\ank22\igv_session.xml 400 BatchScriptName C:\Users\ank22\Documents\SnapShots C:\Users\ank22\Documents\hg002_deepvar_manual_currate.csv C:\IGV_2.5.0\igv.bat 
```

Example with optional parameter:  
```
python batch_igv.py Y:\data\igv_sessions\AndreySession.xml 400 VariantPositionBatch Y:\data\SnapShots C:\Users\ank22\Documents\hg002_deepvar_manual_currate.csv C:\IGV_2.5.0\igv.bat --runScript
```

Example for macOS:
```
python batch_igv.py /Users/sns50/Downloads/macOS_igvsession.xml 400 NewBatchFile /Users/sns50/Documents/SnapShots /Users/sns50/Downloads/hg002_deepvar_manual_currate.csv /Users/sns50/Downloads/IGV_2.5.3/igv.bat --runScript
```
