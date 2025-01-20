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
colors = ['cyan', 'magenta', 'yellow', 'blue', 'green']

# 각 z_axis와 camera_point에 대해 그래프에 추가
# for z_axis, camera_point in zip(z_axes, camera_points):

for i, (z_axis, camera_point) in enumerate(zip(z_axes, camera_points)):
    # z_axis 정규화
    z_axis = z_axis / np.linalg.norm(z_axis)

    # x축과 y축 계산
    x_axis = np.array([1, 0, -z_axis[0] / z_axis[2]])
    x_axis = x_axis / np.linalg.norm(x_axis)
    y_axis = np.cross(z_axis, x_axis)
    y_axis = y_axis / np.linalg.norm(y_axis)

    # 보드 평면 생성 (카메라 시점에서 음수 방향으로 이동)
    board_origin = camera_point - z_axis * scale
    board_x = board_origin + x_axis * scale
    board_y = board_origin + y_axis * scale

    # 보드 평면의 꼭짓점 계산
    board_corners = np.array([
        board_origin,
        board_x,
        board_x + (board_y - board_origin),
        board_y
    ])

    # 보드 평면 플롯
    ax.plot_trisurf(
        board_corners[:, 0], board_corners[:, 1], board_corners[:, 2], 
        # color='cyan', alpha=0.5, label='Board Plane'
        color=colors[i % len(colors)], alpha=0.5, label=f'Board Plane {i + 1}'
    )

# 축 범위 설정
ax.set_xlim([-15, 15])
ax.set_ylim([-15, 15])
ax.set_zlim([-15, 15])

# 축 레이블
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 제목 설정
ax.set_title('3D Board Plane from Camera Perspective')

# 그래프 저장
output_filename = 'board_plane_from_camera.png'
plt.savefig(output_filename, dpi=300, bbox_inches='tight')  # 고해상도 저장

# 그래프 표시
plt.show()

# 저장 완료 메시지
print(f"3D 그래프가 '{output_filename}' 파일로 저장되었습니다.")
