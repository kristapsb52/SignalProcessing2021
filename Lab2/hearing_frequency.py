import matplotlib.pyplot as plt
import skimage.data as data

coins = data.coins()
fig, axes = plt.subplots(1, 2, gridspec_kw={'width_ratios': [1, 2],
                                             'height_ratios': [1, 2]})
axes[0].imshow(coins, extent=[80,120, 32,0])
axes[1].imshow(coins, extent=[40,60,16,0])
plt.show()