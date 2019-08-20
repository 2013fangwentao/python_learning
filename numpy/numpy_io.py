import numpy as np
import matplotlib.pyplot as plt
# import pyproj.proj as proj
import sys
import earth as earth


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
