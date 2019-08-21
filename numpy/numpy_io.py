import numpy as np
import matplotlib.pyplot as plt
import sys
import os

POS_INDEX = 5
VEL_INDEX = 8
ATT_INDEX = 11
TIME_INDEX = 2


def plot_residual(time, pos, vel, att, is_save, save_path):
    plt.figure(1)
    plt.subplot(3, 1, 1)
    plt.plot(time, pos[..., 0])
    plt.ylabel("x(m)")
    plt.subplot(3, 1, 2)
    plt.plot(time, pos[..., 1])
    plt.ylabel("y(m)")
    plt.subplot(3, 1, 3)
    plt.plot(time, pos[..., 2])
    plt.ylabel("z(m)")
    plt.title("pos residual (m)")
    plt.grid()
    if (is_save):
        plt.savefig(os.path.join(save_path, "pos_residual.jpg"))

    plt.figure(2)
    plt.subplot(3, 1, 1)
    plt.plot(time, vel[..., 0])
    plt.ylabel("x(m/s)")
    plt.subplot(3, 1, 2)
    plt.plot(time, vel[..., 1])
    plt.ylabel("y(m/s)")
    plt.subplot(3, 1, 3)
    plt.plot(time, vel[..., 2])
    plt.ylabel("z(m/s)")
    plt.title("vel residual (m/s)")
    plt.grid()
    if (is_save):
        plt.savefig(os.path.join(save_path, "vel_residual.jpg"))

    plt.figure(2)
    plt.subplot(3, 1, 1)
    plt.plot(time, att[..., 0])
    plt.ylabel("x(m/s)")
    plt.subplot(3, 1, 2)
    plt.plot(time, att[..., 1])
    plt.ylabel("y(m/s)")
    plt.subplot(3, 1, 3)
    plt.plot(time, att[..., 2])
    plt.ylabel("z(m/s)")
    plt.title("vel residual (deg)")
    plt.grid()
    if (is_save):
        plt.savefig(os.path.join(save_path, "att_residual.jpg"))
    plt.show()


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
            ''' 角度差异值需要特殊处理一下 '''
            if ((residual_att[residual_i, 2]) > 180):
                residual_att[residual_i, 2] -= 360
            if ((residual_att[residual_i, 2]) < -180):
                residual_att[residual_i, 2] += 360
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
    if (len(sys.argv) < 3):
        print("参数不足")
        return
    if (len(sys.argv) == 3):
        compare(sys.argv[1], sys.argv[2])
    if (len(sys.argv) == 5):
        compare(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    if (len(sys.argv) == 7):
        compare(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]),
                bool(int(sys.argv[5])), sys.argv[6])


if __name__ == "__main__":
    main()
