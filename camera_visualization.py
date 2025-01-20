from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

import numpy as np


z_axis = np.array([0.37036628, 0.48033692, -0.79505047])  # 카메라 z축 방향
camera_point = np.array([4.48271183, 5.81373664, -9.62285811])


# 카메라 x축과 y축을 계산 (z축에 수직한 단위 벡터)
x_axis = np.array([1, 0, -z_axis[0] / z_axis[2]])
x_axis = x_axis / np.linalg.norm(x_axis)  # 정규화
y_axis = np.cross(z_axis, x_axis)  # z축과 x축의 외적
y_axis = y_axis / np.linalg.norm(y_axis)  # 정규화

# # Roll, Pitch, Yaw 계산
# pitch = np.arcsin(-z_axis[1])          # z축의 y-값으로 Pitch 계산
# yaw = np.arctan2(z_axis[0], z_axis[2])  # z축의 x와 z로 Yaw 계산
# roll = np.arctan2(y_axis[2], y_axis[1]) # y축으로 Roll 계산

# # 라디안 -> 도 변환
# pitch_deg = np.degrees(pitch)
# yaw_deg = np.degrees(yaw)
# roll_deg = np.degrees(roll)

# # 결과 출력
# print(f"Pitch: {pitch_deg:.2f} degrees")    # x-axis
# print(f"Yaw: {yaw_deg:.2f} degrees")        # y-axis
# print(f"Roll: {roll_deg:.2f} degrees")      # z-axis



# 카메라 좌표 점 플롯
ax.scatter(camera_point[0], camera_point[1], camera_point[2], color='red', s=100, label='Camera Point')

# 카메라 축 플롯
origin = np.array([0, 0, 0])  # 축의 원점
scale = 5  # 축 길이 스케일
ax.quiver(camera_point[0], camera_point[1], camera_point[2], 
          z_axis[0]*(-1), z_axis[1]*(-1), z_axis[2]*(-1), 
          color='blue', length=scale, label='Z Axis (Camera Front)')
ax.quiver(camera_point[0], camera_point[1], camera_point[2], 
          x_axis[0]*(-1), x_axis[1]*(-1), x_axis[2]*(-1), 
          color='green', length=scale, label='X Axis (Camera Right)')
ax.quiver(camera_point[0], camera_point[1], camera_point[2], 
          y_axis[0]*(-1), y_axis[1]*(-1), y_axis[2]*(-1), 
          color='orange', length=scale, label='Y Axis (Camera Up)')

# 축 범위 설정
ax.set_xlim([camera_point[0] - 10, camera_point[0] + 10])
ax.set_ylim([camera_point[1] - 10, camera_point[1] + 10])
ax.set_zlim([camera_point[2] - 10, camera_point[2] + 10])

# 축 레이블
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 제목과 범례
ax.set_title('3D Camera Coordinate and Axes')
ax.legend()

# 그래프 저장
output_filename = 'camera_axes_plot.png'  # 저장 파일명
plt.savefig(output_filename, dpi=300, bbox_inches='tight')  # 고해상도 저장

# 그래프 표시
# plt.show()

# 저장 완료 메시지
print(f"3D 그래프가 '{output_filename}' 파일로 저장되었습니다.")
