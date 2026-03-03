import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# 1. 配置文件路径
fits_file = '/home/ljiayi/DRAGON2-Beta_version-master/output/test1.fits.gz'
Ekmin = 0.1
Ekfactor = 1.2
num_energies = 65
energies = Ekmin * (Ekfactor ** np.arange(num_energies))

fig, ax2 = plt.subplots(figsize=(10, 6))

# 我们用来画图的颜色，按顺序画出通量最大的前 2 个粒子
colors = ['blue', 'green']
plot_count = 0

print("=== 正在暴力搜索非空图层 ===")

with fits.open(fits_file) as hdul:
    # 记录每个图层的最大通量，用来排序找质子
    max_fluxes = []
    
    for i in range(len(hdul)):
        data = hdul[i].data
        if data is not None:
            # 提取 Z=0, R=8.3 的地球附近通量
            flux_R8 = data[40, 28, :]
            layer_max = np.max(flux_R8)
            
            # 如果最大值大于一个极小数，说明这层有真实数据
            if layer_max > 1e-15:
                max_fluxes.append((i, layer_max))
    
    # 按通量大小从高到低排序 (质子绝对是排第一的)
    max_fluxes.sort(key=lambda x: x[1], reverse=True)
    
    if not max_fluxes:
        print("❌ 灾难性错误：整个文件里所有的 52 层数据全都是 0！")
        print("这说明你的 DRAGON 模拟虽然生成了文件，但粒子没有注入成功。")
        exit()

    print(f"\n✅ 搜索完毕！通量最高的图层是 HDU [{max_fluxes[0][0]}]，最大通量: {max_fluxes[0][1]:.2e} (这肯定是质子！)")