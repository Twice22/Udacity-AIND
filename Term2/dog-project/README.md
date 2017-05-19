# Udacity AIND: dog-project 

## Installation instructions
1. Clone the repository and navigate to the downloaded folder.
	```	
		git clone https://github.com/Twice22/Udacity-AIND.git
		cd dog-project
	```

2. Install the necessary Python packages.
	
	For __Mac/OSX__ (Option 2):
	```
		conda env create -f requirements/aind-dog-mac.yml
		source activate aind-dog
	```

	For __Windows__:
	```
		conda env create -f requirements/aind-dog-windows.yml
		activate aind-dog
	```
	
3. (Optional: if you have an nvidia GPU) Install GPU version of TensorFlow
    1. First you need to uninstall tensorflow with:
        ```shell
         pip uninstall tensorflow
        ```
   2. Then See my tutorial [here](https://twice22.github.io/tensorflow/ "How to Install TensorFlow") on how to install            TensorFlow
4. Download and install the datasets:
    1. download the [dog dataset](https://s3-us-west-1.amazonaws.com/udacity-aind/dog-project/dogImages.zip), unzip the            folder and place it in the repo, at location `path/to/dog-project/dogImages`.
    2. download the [human dataset](http://vis-www.cs.umass.edu/lfw/lfw.tgz). Unzip the folder and place it in the repo, at        `location path/to/dog-project/lfw`.
    3. download the [VGG-16 bottleneck features](https://s3-us-west-1.amazonaws.com/udacity-aind/dog-project/DogVGG16Data.npz) for the dog dataset. Place it in the repo, at location `path/to/dog-project/bottleneck_features`.

**Note**: I have a GTX1060 with 6GB, and training a CNN on my GPU is about **5x** faster than training on my CPU!

## Issues
1. _Jupyter Notebook Freeze while training_. See the solution I posted on the Udacity Forum [here](https://discussions.udacity.com/t/jupyter-notebook-freeze-while-training-solution/247335 "Solution")
2. _I installed tensorflow-gpu but I cannot import tensorflow_. You probably need to install [Microsoft Visual C++ 2015 Redistributable](https://www.microsoft.com/en-us/download/details.aspx?id=53840 "Microsoft Visual C++ 2015). Also you need to be sure I've installed `cuDNN 5.1`. As of now, TensorFlow **still doesn't support cuDNN 6**
3. _Some of the codes don't work_. It might be because you didn't install the datas, or you need to create the datas. For example for the **Optional part** of the assignment, if you want to run my code you need to:
    - download the [caltech256 dataset](http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar)         and to extract the archive to `location path/to/dog-project`.
    - rename the extracted folder to `caltech256`.
    - erase **dog** and **easy-face** folders from `caltech256` folder

4. _saved_models/weights.best.restnet50_faces.hdf5 is missing_. You need to **Uncomment** the commented code under the **Option Part : Training DNN for face detection**



