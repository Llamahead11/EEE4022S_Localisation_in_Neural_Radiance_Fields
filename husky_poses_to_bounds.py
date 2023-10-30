import numpy as np
import os

def rotate_pose_z_90_degrees(pose):
    R = pose[:3, :3]
    # Create a rotation matrix for a 90-degree rotation around the Z-axis
    rotation_matrix = np.array([[0, 1, 0],
                                [0, 0, 1],
                                [-1, 0, 0]])
    # Apply the rotation to the original rotation matrix
    new_R = R.dot(rotation_matrix)
    # Update the pose with the rotated orientation
    pose[:3, :3] = new_R

# Path to the folder containing the text files
folder_path = '/home/dominic/nerf-pytorch/data/nerf_llff_data/husky/poses'

# List all files in the folder
files_in_folder = os.listdir(folder_path)
focal_length  = 531
# Filter only text files (you can adjust this filter as needed)
#text_files = [file for file in files_in_folder if file.endswith('.txt')]
text_files = sorted([f for f in os.listdir(folder_path) if (os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.txt'))], key=lambda x: int(''.join(filter(str.isdigit, os.path.splitext(x)[0]))))
#print(text_files)
# Read each text file
poses = []
basedir = '/home/dominic/inerf/data/nerf_llff_data/husky/'
image_num = 0
transformation = []
for text_file in text_files:
    #print(text_file)
    file_path = os.path.join(folder_path, text_file)
    with open(file_path, 'r') as file:
        # Read the contents of the file
        if image_num < 900:
            file_contents = file.read()
            SE3 = np.array(file_contents.split()).reshape(4,-1).astype(float)
        
            '''
            #flip third column -1
            third_column = np.array(SE3[:, 2])
            #print(third_column)
            third_column = third_column.astype(float)
            #print(third_column)
            rectified_col = ([-1, -1, -1, 1] * third_column)
            SE3[:, 2] = (rectified_col)
            '''
            if image_num == 115:
                print(SE3)
            #SE3 = np.linalg.inv(SE3)

            xyz_col = np.multiply(SE3[:,3], [1, -1, -1, 1])
            SE3[:,3] = xyz_col

            if image_num == 115:
                print(SE3)
            rotation_matrix = SE3[0:3,0:3].T
            SE3[0:3,0:3] = rotation_matrix

            SE3_copy = np.copy(SE3)

            SE3 = np.concatenate([-SE3[2:3, :], -SE3[0:1, :], SE3[1:2, :], SE3[3:,:]], 1)
            SE3 = SE3.reshape(4,4)
            #print(SE3)
            rotate_pose_z_90_degrees(SE3)
            

            intrinsics = np.array([[720/4],[1280/4],[focal_length]]) #`[image height, image width, focal length]`
            concatenated_matrix = np.hstack((SE3[0:3].reshape(3,-1), intrinsics))
            depth_vals = np.array([0.5, 20])
            poses.append(np.concatenate([concatenated_matrix.ravel(), depth_vals], 0))
            if image_num % 20 == 0:
                transformation.append(SE3_copy)
                print(poses[image_num])


    image_num = image_num + 1
poses = np.array(poses)
poses = poses.astype(float)
np.save(os.path.join(basedir, 'poses_bounds.npy'), poses[0:841])

#sd_data = np.load('/home/aap/catkin_ws/src/Loc-NeRF/logs/inerf_compare/pos_time.npy')
#print(sd_data)

# Load the .npy file
data = np.load('/home/dominic/inerf/data/nerf_llff_data/husky/poses_bounds.npy')
# Print the data
#print(data[343])
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


transformation= np.array(transformation)
#transformation = np.concatenate([transformation[:, 1:2, :], -transformation[:, 0:1, :], transformation[:, 2:, :]],1)
#transformation = np.concatenate([transformation[:, 1:2, :], transformation[:, 0:1, :], transformation[:, 2:3, :], transformation[:,3:,:]], 1)
transformation = np.concatenate([-transformation[:, 2:3, :], -transformation[:, 0:1, :], transformation[:, 1:2, :], transformation[:,3:,:]], 1)

# Apply the rotation to each pose in the 'poses' array
for i in range(transformation.shape[0]):
    rotate_pose_z_90_degrees(transformation[i])

# Create a 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Extract the translation vectors from the poses
translations = transformation[:, :3, 3]

# Extract the orientation vectors (X-axis) from the poses
orientations = transformation[:, :3, 0]

# Plot the positions as points
ax.scatter(translations[:, 0], translations[:, 1], translations[:, 2], c='r', marker='o', label='Positions')

# Plot the orientations as arrows
ax.quiver(translations[:, 0], translations[:, 1], translations[:, 2],
          orientations[:, 0], orientations[:, 1], orientations[:, 2],
          color='b', label='Orientations', pivot='tail')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set axis limits (adjust as needed)
ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])
ax.set_zlim([-10, 10])

# Add a legend
ax.legend()

# Show the plot
plt.show()