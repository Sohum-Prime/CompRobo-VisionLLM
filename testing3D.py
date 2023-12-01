import open3d as o3d
import numpy as np
from scipy.spatial import KDTree

# load .ply file
point_cloud = o3d.io.read_point_cloud('/Users/zaynpatel/vision/visionLLM/CompRobo-VisionLLM/ply files/Wall1_point_cloud.ply')
point_cloud2 = o3d.io.read_point_cloud('/Users/zaynpatel/vision/visionLLM/CompRobo-VisionLLM/ply files/Wall2_point_cloud.ply')

downsampled_point_cloud = point_cloud.voxel_down_sample(voxel_size=0.05) # point cloud 1 (what does this voxel_down_sample do?)
downsampled_point_cloud2 = point_cloud2.voxel_down_sample(voxel_size=0.05) # point cloud 2 (what does this voxel_down_sample do?)

clean_point_cloud, ind = downsampled_point_cloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0) # downsampled point cloud 1 (what does this downsampling do?)
cloud_point2, ind2 = downsampled_point_cloud2.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0) # downsampled point cloud 2 (what does this downsampling do?)

keypoints = o3d.geometry.keypoint.compute_iss_keypoints(point_cloud) # iss keypoints point cloud 1 (what are these?)
keypoints2 = o3d.geometry.keypoint.compute_iss_keypoints(point_cloud2) # iss keypoints point cloud 2 (what are these?)

# Estimate normals
downsampled_point_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
downsampled_point_cloud2.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

init_transform = np.identity(4)

icp_result = o3d.pipelines.registration.registration_icp(
    point_cloud, point_cloud2, max_correspondence_distance=0.05, 
    init=init_transform,
    estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint())

transformed_point_cloud = point_cloud.transform(icp_result.transformation)

# Compute FPFH features
fpfh = o3d.pipelines.registration.compute_fpfh_feature(
    downsampled_point_cloud,
    o3d.geometry.KDTreeSearchParamHybrid(radius=0.25, max_nn=100))

fpfh2 = o3d.pipelines.registration.compute_fpfh_feature(
    downsampled_point_cloud2, 
    o3d.geometry.KDTreeSearchParamHybrid(radius=0.25, max_nn=100)
)

np.save('fpfh_features.npy', np.asarray(fpfh.data).T)
np.save('fpfh2_features.np', np.asarray(fpfh2.data).T)

fpfh_features = np.asarray(fpfh.data) # we want data from the fpfh features to use here (why?)
fpfh_features2 = np.asarray(fpfh2.data)

tree1 = KDTree(fpfh_features.T)
tree2 = KDTree(fpfh_features2.T)

for i in range(fpfh_features2.shape[1]):
    point_feature = fpfh_features2[:, i]
    dist, index = tree1.query(point_feature)
    print(f"Point {i} in cloud 2 is closest to point {index} in cloud 1 with distance {dist}")