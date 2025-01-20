from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# 입력 데이터: 여러 z_axis와 camera_point 값
z_axes = [

np.array([ 0.35290849, 0.28558361, -0.89100932]),
np.array([-0.11659692, 0.40322878, -0.90764074]),
np.array([ 0.07062387, 0.26945394, -0.96042014]),
np.array([ 0.17449294, 0.76876565, -0.61526546]),
np.array([-0.39414439, 0.33670623, -0.85514859])
]
camera_points = [
np.array([ 1.57998955, 1.2785726, -3.98909479]),
np.array([-1.00974439, 3.49201323, -7.86028589]),
np.array([  1.18900633, 4.53646103, -16.16940012]),
np.array([ 1.61248972, 7.10416559, -5.6856699 ]),
np.array([-4.38025369, 3.74192491, -9.50354216])
]
# 그래프 설정
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 스케일 설정
scale = 5

# 각 z_axis와 camera_point에 대해 그래프에 추가
for z_axis, camera_point in zip(z_axes, camera_points):
    # z_axis 정규화
    z_axis = z_axis / np.linalg.norm(z_axis)

    # x축과 y축 계산
    x_axis = np.array([1, 0, -z_axis[0] / z_axis[2]])
    x_axis = x_axis / np.linalg.norm(x_axis)
    y_axis = np.cross(z_axis, x_axis)
    y_axis = y_axis / np.linalg.norm(y_axis)

    # 카메라 좌표 점 플롯
    ax.scatter(camera_point[0], camera_point[1], camera_point[2], color='red', s=100, label='Camera Point')

    # 카메라 축 플롯
    ax.quiver(camera_point[0], camera_point[1], camera_point[2], 
              z_axis[0] * (-1), z_axis[1] * (-1), z_axis[2] * (-1), 
              color='blue', length=scale, label='Z Axis')
    ax.quiver(camera_point[0], camera_point[1], camera_point[2], 
              x_axis[0] * (-1), x_axis[1] * (-1), x_axis[2] * (-1), 
              color='green', length=scale, label='X Axis')
    ax.quiver(camera_point[0], camera_point[1], camera_point[2], 
              y_axis[0] * (-1), y_axis[1] * (-1), y_axis[2] * (-1), 
              color='orange', length=scale, label='Y Axis')

# 축 범위 설정
ax.set_xlim([-15, 15])
ax.set_ylim([-15, 15])
ax.set_zlim([-15, 15])

# 축 레이블
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 제목 설정
ax.set_title('3D Camera Coordinates and Axes')

# 범례 (중복 제거)
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

# 그래프 저장
output_filename = 'multiple_camera_axes_plot.png'
plt.savefig(output_filename, dpi=300, bbox_inches='tight')  # 고해상도 저장

# 그래프 표시
plt.show()

# 저장 완료 메시지
print(f"3D 그래프가 '{output_filename}' 파일로 저장되었습니다.")
