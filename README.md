# Automatic Parking-Space-Allocation
### Step 1
Create a folder for example <folder_name> and put 2 files into it. Image or video and its corresponding YAML file. 

In yaml file copy the following lines-

  - four_corners : <folder_name>/four_corners_cordinate.yaml
  
  - rectangle_cordinates: <folder_name>/rectangle_cordinates.yaml
  
### Step 2
Run video_bounding_box_v2.py.

To select the parking lot region type-

  - python video_bounding_box_v2.py --four_corners --source <image file_name>.jpg -- data <yaml file name>.yaml 

To select the corresponding rectangular type - 
  
  - python video_bounding_box_v2.py --rectangles --source <imgae file_name>.jpg --data <yaml file name>.yaml

### Step 3

Run detectV3.py.

Your result will be saved in runs/detect/exp<no.> folder
