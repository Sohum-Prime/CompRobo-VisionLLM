import open3d as o3d
import numpy as np
from scipy.spatial import KDTree
# downside for this is computational efficiency
from itertools import combinations # use this library to see all the pairs we can potentially iterate over to compare point clouds

# using * so I can take in multiple point clouds as arguments
# the type of these point clouds would be .ply files
def check_point_cloud_distances(file_paths):
    processed_point_cloud = [] # list holds the points and their differences
    for files in file_paths:
        point_cloud = o3d.io.read_point_cloud(files)

        # voxel grid is a 3D grid of values organized into rows and columns
        # we downsample the point cloud to make the computation more efficient by looking at points that might be redundant 
        # we do this based on the pooling method (is this a hyperparam?) which, in average pooling, means we take the average pixel values of the feature map and use those
        downsampled_point_cloud = point_cloud.voxel_down_sample(voxel_size=0.05) # state: take the two point clouds whose data I've read and reduce their points to 0.05 which means that each voxel cube has 0.05 units.
        clean_point_cloud, ind = downsampled_point_cloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0) # downsampled point cloud 1 (what does this downsampling do?)
        keypoints = o3d.geometry.keypoint.compute_iss_keypoints(clean_point_cloud) # retain key features without losing critical geometric information
        # Estimate normals
        downsampled_point_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
        
        init_transform = np.identity(4)
        icp_result = o3d.pipelines.registration.registration_icp(
        point_cloud, max_correspondence_distance=0.05, 
        init=init_transform,
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint())
        transformed_point_cloud = point_cloud.transform(icp_result.transformation)

        # Compute FPFH features
        # These FPFH features capture local properties around a point and then create a histogram of values based on surface normals/neighbors
        fpfh = o3d.pipelines.registration.compute_fpfh_feature(
            transformed_point_cloud,
            o3d.geometry.KDTreeSearchParamHybrid(radius=0.25, max_nn=100))

        processed_point_cloud.append((clean_point_cloud, keypoints, fpfh))
    return processed_point_cloud

def comparing_point_clouds(processed_point_cloud):
    # state: we have a processed point cloud and we want to compare multiple points
    # this means we need an iterator for multiple things
    # use enumerate because I want to get a unique tree using KDTree each time and doing this with just a variable will over write it each loop
    # so I need some persisting data structure -> I'm using a dictionary to hold all KDTrees which I can create pairs out of and iterate on after
    tree_dict = {}
    fpfh_features_dict = {}
    for index, item in enumerate(processed_point_cloud): # state: this is just iterating through the point cloud tuples, I need another iterator to compare two given tuples that haven't been compared before
        clean_point_cloud, keypoints, fpfh = item # use tuple unpacking so I can use the items in the processed_point_cloud
        fpfh_features = np.asarray(fpfh.data) # actual spatial features
        fpfh_features_dict[index] = fpfh_features
        tree_dict[index] = KDTree(fpfh_features) # this is a data structure that makes queries on features simpler but doesn't actually contain features
    
    #print(tree_dict)
    #print(f'this is the fpfh_features dictionary: {fpfh_features_dict}')
    # args: combinations(what do you want to combine, how many in each combination?) - use index + 1 so we encompass all point clouds
    point_cloud_pairs = list(combinations(range(len(processed_point_cloud)), 2))
    # these are two point clouds - we want to iteratively retrieve them so we can compare
    for index1, index2 in point_cloud_pairs:
        # need these two because we are always only comparing two no matter combinations
        tree1 = tree_dict[index1] # these are KD-Tree objects that correspond to point clouds at the point_cloud1, point_cloud2 indices
        tree2 = tree_dict[index2]
        for feature in fpfh_features_dict[index1]:
            print(len(feature))
            tree2.query(feature)
        for feature in fpfh_features_dict[index2]:
            tree1.query(feature) 
            print(len(feature))  

# Call functions 
file_paths = ['/Users/zaynpatel/vision/visionLLM/CompRobo-VisionLLM/ply files/Wall1_point_cloud.ply', '/Users/zaynpatel/vision/visionLLM/CompRobo-VisionLLM/ply files/Wall2_point_cloud.ply', '/Users/zaynpatel/vision/visionLLM/CompRobo-VisionLLM/ply files/Wall3_point_cloud.ply']
testing = check_point_cloud_distances(file_paths)
test = comparing_point_clouds(testing) # pass the output from the check_point_cloud_distances as input
print(test)