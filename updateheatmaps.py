import psycopg2
import numpy as np

from heatmap import heatmap, normalize

# Reads in the connection info
args = dict()
with open('db_info.txt', 'r') as f:
    for line in f:
        key, value = line.split('=')
        args[key] = value.strip()

# Connect to the database
con = psycopg2.connect(**args)

# Opens a cursor to perform database operations
cur = con.cursor()

# these are the ranges for the x and y axis.
rx = (-2.45, 2.35)
ry = (-0.75, 5)

# these are the ranges for the strike zone
strike_x = (-0.86, 0.86)
strike_y = (1.59, 3.13)

# calculates the resolution of the heatmap. res is the maximum resolution
# of either axis. resx and resy are the calculated resolutions for the x and y
# where 
# the aspect ratio is preserved.
res = 20
resx = int(res / max(rx[1] - rx[0], ry[1] - ry[0]) * (rx[1] - rx[0]))
resy = int(res / max(rx[1] - rx[0], ry[1] - ry[0]) * (ry[1] - ry[0]))

team_name = 'AUB_TIG'
pitcher_names = ['MyersCarson', 'BaumanTanner', 'GravesGriffin', 'SofieldDrew', 'KeplingerKonner', 'CopelandKonner', 'CrotchfeltZach', 'NelsonDrew', 'SchorrBen', 'WattsDylan', 'CarlsonParker', 'HerberholzChristian', 'CannonWill', 'McBrideConner', 'TillyCam', 'ArmstrongJohn', 'PetrovicAlex', 'GonzalezJoseph', 'AllsupChase', 'KeshockCameron', 'MurphyHayden']
pitch_types = ['Fastball', 'Slider', 'ChangeUp', 'FourSeamFastBall', 'Sinker', 'Curveball', 'Cutter', 'Splitter', 'TwoSeamFastBall']

success = ['StrikeCalled', 'StrikeSwinging', 'FoulBall']

for pitcher in pitcher_names:
    all_types_hmap = np.zeros((resy, resx))
    all_types_hmap_all = np.zeros((resy, resx))
    for pitch_type in pitch_types:
        cur.execute(f"""SELECT trackman_pitcher."PlateLocHeight", trackman_pitcher."PlateLocSide", trackman_metadata."PitchCall" 
                    FROM trackman_pitcher 
                    INNER JOIN trackman_metadata ON trackman_pitcher."PitchUID" = trackman_metadata."PitchUID"
                    WHERE trackman_pitcher."Pitcher" = '{pitcher}' 
                    AND trackman_pitcher."PitcherTeam" = '{team_name}'
                    AND trackman_pitcher."TaggedPitchType" = '{pitch_type}';""")
        values = cur.fetchall()

        print(len(values))
        values = [(float(row[0]), float(row[1]), 1.0 if row[2] in success else 0.0) for row in values]
        values_all = [(row[0], row[1], 1) for row in values]

        hmap = heatmap(values, resx, resy, spr=0.55, range_x=rx, range_y=ry)
        hmap_all = heatmap(values_all, resx, resy, spr=0.55, range_x=rx, range_y=ry)
        hmap_ratio = hmap / (hmap_all + 1e-6)

        all_types_hmap += hmap
        all_types_hmap_all += hmap_all

        hmap = normalize(hmap)
        hmap_all = normalize(hmap_all)
        hmap_ratio = normalize(hmap_ratio)

        # Write the heatmaps to the database

    all_types_hmap = all_types_hmap
    all_types_hmap_all = all_types_hmap_all
    all_types_hmap_ratio = all_types_hmap / (all_types_hmap_all + 1e-6)

    all_types_hmap = normalize(all_types_hmap)
    all_types_hmap_all = normalize(all_types_hmap_all)
    all_types_hmap_ratio = normalize(all_types_hmap_ratio)

    # Write the heatmaps for all pitch types to the database


# Close communication with the database
cur.close()
con.close()
