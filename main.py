import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
print(baseball_data.tail())

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

gravesdata = baseball_data[baseball_data['Pitcher'] == 'Graves, Griffin']

res = 15
heatmap = [[0 for i in range(res)] for j in range(res)]
heatmap_hit = [[0 for i in range(res)] for j in range(res)]
minh_keep = 1
maxh_keep = 3.5
minw_keep = -1.5
maxw_keep = 1.5
spr = 0.25
offsets = [(0,0,1), (0,1,spr), (1,1,spr), (1,0,spr), (1,-1,spr), (0,-1,spr), (-1,-1,spr), (-1,0,spr), (-1,1,spr)]
for index, row in gravesdata.iterrows():
    h = row['PlateLocHeight']
    s = row['PlateLocSide']
    if minh_keep <= h <= maxh_keep and minw_keep <= s <= maxw_keep:
        h = int((h - minh_keep) / (maxh_keep - minh_keep) * res)
        s = int((s - minw_keep) / (maxw_keep - minw_keep) * res)
        for offset in offsets:
            h2 = h + offset[0]
            s2 = s + offset[1]
            if 0 <= h2 < res and 0 <= s2 < res:
                heatmap[h2][s2] += 1*offset[2]
                heatmap_hit[h2][s2] += row['PitchCall']*offset[2]

#plt.imshow(heatmap, cmap='hot', interpolation='nearest')
#plt.show()
plt.imshow(heatmap_hit, cmap='hot', interpolation='nearest')
plt.show()

