import numpy as np
import matplotlib.pyplot as plt
# import pyproj.proj as proj
import sys
import earth as earth

POS_INDEX = 5
VEL_INDEX = 8
ATT_INDEX = 11
TIME_INDEX = 2


def plot_residual(time, pos, vel, att, is_save, save_path):
    plt.figure(1)
    plt.subplot(3, 1, 1)
    plt.plot(time, pos[..., 0])
    plt.ylabel("x(m)")


def compare(result_file,
            truth_file,
            start_time=0,
            end_time=86400,
            is_save_picture=False,
            save_path="./"):
    result_data = np.loadtxt(result_file)
    truth_data = np.loadtxt(truth_file)
    data_index = result_data[..., TIME_INDEX] > start_time and result_data[
        ..., TIME_INDEX] < end_time
    refer_index = truth_data[..., TIME_INDEX] > start_time and truth_data[
        ..., TIME_INDEX] < end_time
    data_time = result_data[data_index, TIME_INDEX]
    pos_data = result_data[data_index, POS_INDEX:POS_INDEX + 3]
    vel_data = result_data[data_index, VEL_INDEX:VEL_INDEX + 3]
    att_data = result_data[data_index, ATT_INDEX:ATT_INDEX + 3]

    ref_time = truth_data[refer_index, TIME_INDEX]
    ref_pos_data = truth_data[refer_index, POS_INDEX:POS_INDEX + 3]
    ref_vel_data = truth_data[refer_index, VEL_INDEX:VEL_INDEX + 3]
    ref_att_data = truth_data[refer_index, ATT_INDEX:ATT_INDEX + 3]

    ref_i = 0
    data_i = 0
    residual_i = 0
    residual_pos = np.nan(pos_data.shape)
    residual_vel = np.nan(vel_data.shape)
    residual_att = np.nan(att_data.shape)
    residual_time = np.nan(ref_time.shape)
    while (data_i < np.size(data_time) and ref_i < np.size(ref_time)):
        if (np.abs(ref_time[ref_i] - data_time[data_i]) < 5.5e-2):
            residual_pos[residual_i, ...] = ref_pos_data[
                ref_i, ...] - pos_data[data_i, ...]
            residual_vel[residual_i, ...] = ref_vel_data[
                ref_i, ...] - vel_data[data_i, ...]
            residual_att[residual_i, ...] = ref_att_data[
                ref_i, ...] - att_data[data_i, ...]
            residual_time[residual_i] = ref_time[ref_i]
            ref_i += 1
            data_i += 1
            residual_i += 1
        elif (ref_time[ref_i] - data_time[data_i] > 0):
            data_i += 1
        else:
            ref_i += 1
    residual_pos = residual_pos[~np.isnan(residual_pos)]
    residual_vel = residual_vel[~np.isnan(residual_vel)]
    residual_att = residual_att[~np.isnan(residual_att)]

    pos_mean = np.zeros([3, 3])
    vel_mean = np.zeros([3, 3])
    att_mean = np.zeros([3, 3])

    pos_mean[0, ...] = np.mean(residual_pos)
    vel_mean[0, ...] = np.mean(residual_vel)
    att_mean[0, ...] = np.mean(residual_att)

    pos_mean[1, ...] = np.std(residual_pos)
    vel_mean[1, ...] = np.std(residual_vel)
    att_mean[1, ...] = np.std(residual_att)

    pos_mean[2, ...] = np.sqrt(pos_mean[0, ...] * pos_mean[0, ...] +
                               pos_mean[1, ...] * pos_mean[1, ...])
    vel_mean[2, ...] = np.sqrt(vel_mean[0, ...] * vel_mean[0, ...] +
                               vel_mean[1, ...] * vel_mean[1, ...])
    att_mean[2, ...] = np.sqrt(att_mean[0, ...] * att_mean[0, ...] +
                               att_mean[1, ...] * att_mean[1, ...])
    plot_residual(residual_time, residual_pos, residual_vel, residual_att,
                  is_save_picture, save_path)


def main():
    print("length of argv is %d" % len(sys.argv))
    if (len(sys.argv) < 2):
        print("参数不足")
        return

    file_path = sys.argv[1]  # 结果文件
    pos_data = np.loadtxt(file_path)
    time = pos_data[..., 1]
    xyz = pos_data[..., 2:5]
    vxyz = pos_data[..., 5:8]
    att = pos_data[..., 8:11]
    blh = earth.array_xyz2blh(xyz)
    xyz_mean = np.mean(xyz, axis=0)
    xyz = xyz - xyz_mean
    plt.figure(1)
    plt.title("xyz")
    plt.plot(time, xyz)
    plt.ylabel("xyz(m)")
    plt.xlabel("time(s)")
    plt.grid()
    # plt.show()

    plt.figure(2)
    plt.title("vxyz")
    plt.plot(time, vxyz)
    plt.ylabel("vxyz(m)")
    plt.xlabel("time(s)")
    plt.grid()
    # plt.show()

    plt.figure(3)
    plt.title("att")
    plt.plot(time, att)
    plt.ylabel("att(deg)")
    plt.xlabel("time(s)")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
