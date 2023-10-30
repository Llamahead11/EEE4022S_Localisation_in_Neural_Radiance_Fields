import json
import os
import numpy as np

def read_poses_from_folder_and_populate_frame_array(folder_path):
    # Get a list of all files in the folder
    #files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    files = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))], key=lambda x: int(''.join(filter(str.isdigit, os.path.splitext(x)[0]))))

    # Initialize an empty list to store poses
    all_poses = []
    image_num = 28

    for file in files:
        # Check if the file is a text file
        if file.endswith('.txt') and 28 <= image_num < 869:
            if image_num % 1 == 0 or image_num == 28:
                file_path = os.path.join(folder_path, file)
                with open(file_path, 'r') as f:
                    # Read lines from the file and parse poses
                    lines = f.readlines()
                    poses = []
                    line_num = 0
                    for line in lines:
                        if line_num < 4:
                            # Assume poses are space-separated values
                            pose_values = line.strip().split()
                            # Convert pose values to float and append to the list
                            poses.append([float(val) for val in pose_values])
                        line_num = line_num + 1
                    poses = np.array(poses)
                    check = [0.030005188658833504, -0.4170617163181305, 0.1823979765176773]
                    if np.any(poses[3, 0:3] == check):
                        print(image_num)
                       
                    xyz_col = poses[:,3]
                    poses[:,3] = np.multiply(xyz_col,[1, -1, -1, 1])
                    '''
                    #rot_col = poses[:,2]
                    third_row = poses[2,:]
                    
                    #poses[:,2] = np.multiply(rot_col,[-1, -1, -1, 1])
                    #poses[:,2] = np.multiply(xyz_col,[1, 1, 1, 1])
                    poses[2,:] = np.multiply(third_row,[-1,-1,-1, 1])
                    
                    '''
                    
                    #print(poses[0:3,0:3])
                    rotation_matrix = poses[0:3,0:3].T
                    poses[0:3,0:3] = rotation_matrix
                    poses = poses.tolist()
                    # Append the poses from this file to the list of all poses
                    all_poses.append({"file_path": "./images_4/{}.png".format(image_num),"transform_matrix": poses})
            image_num = image_num + 1


    # Convert the list of poses to a NumPy array
    #poses_array = np.array(all_poses)

    return all_poses

# Example usage
folder_path = '/notebooks/nerfstudio/data/nerfstudio/husky/poses'
frames = read_poses_from_folder_and_populate_frame_array(folder_path)

# Print the poses array
#print('Poses array:')
#print(frames)
'''
frames = [
        {
            "file_path": "./images/frame_00001.png",
            "transform_matrix": [
                [0.32316911338447335, -0.8052290294881217, -0.4971598678734143, -0.7282161659858809],
                [-0.43978339113907267, 0.33738608648128665, -0.8323227724429142, -2.7487404236023076],
                [0.8379452804524355, 0.48762366505170673, -0.24509359079549578, -2.1384913608645126],
                [0.0, 0.0, 0.0, 1.0]
            ]
        },
        # Add more frames in a similar structure
        # ...
    ]
'''
# Create the data structure as per the specified format

data = {
    "fl_x": 531.14774/4,
    "fl_y": 531.26312/4,
    "k1": 0,
    "k2": 0,
    "k3": 0,
    "k4": 0,
    "p1": 0,
    "p2": 0,
    "cx": 640/4,
    "cy": 360/4,
    "w": 1280/4,
    "h": 720/4,
    "aabb_scale": 16,
    "frames": frames
}

# Save the data to a JSON file
with open("/notebooks/content_4/transforms.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("JSON data written to transforms.json")