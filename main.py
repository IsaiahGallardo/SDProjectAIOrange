import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from heatmap import heatmap

baseball_data = pd.read_csv('TrackMan_NoStuff_Master.csv')
baseball_data = baseball_data[['Pitcher', 'Batter', 'PitchCall', 'PlateLocHeight', 'PlateLocSide']]
print(baseball_data.tail())

baseball_data.loc[baseball_data["PitchCall"] == "StrikeCalled", "PitchCall"] = 1
baseball_data.loc[baseball_data["PitchCall"] == "StrikeSwinging", "PitchCall"] = 1
baseball_data.loc[baseball_data["PitchCall"] == "BallCalled", "PitchCall"] = 0
baseball_data.loc[baseball_data["PitchCall"] == "FoulBall", "PitchCall"] = 1
baseball_data.loc[baseball_data["PitchCall"] == "InPlay", "PitchCall"] = 0
baseball_data.loc[baseball_data["PitchCall"] == "HitByPitch", "PitchCall"] = 0
baseball_data.loc[baseball_data["PitchCall"] == "BallinDirt", "PitchCall"] = 0
baseball_data.loc[baseball_data["PitchCall"] == "Undefined", "PitchCall"] = 0
baseball_data.loc[baseball_data["PitchCall"] == "BallInDirt", "PitchCall"] = 0

minh = min(baseball_data['PlateLocHeight'])
maxh = max(baseball_data['PlateLocHeight'])
minw = min(baseball_data['PlateLocSide'])
maxw = max(baseball_data['PlateLocSide'])
print('min H: ', minh)
print('max H: ', maxh)
print('min W: ', minw)
print('max W: ', maxw)

baseball_data['PitchCall'] = baseball_data['PitchCall'].astype(int)
baseball_data['PitchCall'].value_counts()

# removes outliers based on 3 standard deviations from mean -- don't have to use!!
new_df = baseball_data[(baseball_data['PlateLocSide'] < 2.7) & (baseball_data['PlateLocSide'] > -2.8)]
new_df = new_df[(new_df['PlateLocHeight'] < 5.4) & (new_df['PlateLocHeight'] > -0.8)]


gravesdata = baseball_data[baseball_data['Pitcher'] == 'Graves, Griffin']

# these are the ranges for the x and y axis. cuttoff were chosen 
# somewhat arbitrarily based on the observed spread of the data
rx = (1, 3.5)
ry = (-1.5, 1.5)

# calculates the resolution of the heatmap. res is the maximum resolution
# of either axis. resx and resy are the calculated resolutions for the x and y
# where the aspect ratio is preserved.
res = 20
resx = int(res / max(rx[1] - rx[0], ry[1] - ry[0]) * (rx[1] - rx[0]))
resy = int(res / max(rx[1] - rx[0], ry[1] - ry[0]) * (ry[1] - ry[0]))

values = [(row['PlateLocHeight'], row['PlateLocSide'], row['PitchCall']) for index, row in gravesdata.iterrows()]
hmap = heatmap(values, resx, resy, spr=0.25, range_x=rx, range_y=ry)

plt.imshow(hmap, cmap='hot', interpolation='nearest', origin='lower', extent=(rx[0], rx[1], ry[0], ry[1]))
plt.show()

