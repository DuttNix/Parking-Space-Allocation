# Automatic Parking-Space-Allocation

### To run this project do the following- 

#### Step 1 

git clone https://github.com/nixondutt/Parking-Space-Allocation

#### Step 2

python detectV3.py

Result will be saved in runs/detect/exp<no.> folder 

## To create your own Parking Lot System

### Step 1
Create a folder for example <folder_name> and put 2 files into it. Image or video and its corresponding YAML file. 

In yaml file copy the following lines-

  - four_corners : <folder_name>/four_corners_cordinate.yaml
  
  - rectangle_cordinates: <folder_name>/rectangle_cordinates.yaml
  
### Step 2
Return to parking space allocation folder and run video_bounding_box_v2.py.

To select the parking lot regions type-

  - python video_bounding_box_v2.py --four_corners --source <image file_name>.jpg -- data [yamlfile name].yaml 

This will create a yaml file namly **four_corners_cordinate.yaml** inside the created folder.
 
ps - At each region of interest put id number from command line

To select the corresponding rectangular type - 
  
  - python video_bounding_box_v2.py --rectangles --source <imgae file_name>.jpg --data [yamlfile name].yaml

This will create a yaml file namly **rectangle_cordinate.yaml** inside the created folder.

ps - At each region of interest put same id number as previous time. The id's must be same for both **four_corners_cordinate.yaml file** and **rectangle_cordinates_yaml file**.

### Step 3

Run detectV3.py.

Your result will be saved in runs/detect/exp<no.> folder
