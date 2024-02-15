

def heatmap(values, res_x, res_y, spr=0.25, range_x=None, range_y=None):
    """
    Create a heatmap from a list of values.

    values: list of values, where each value is a tuple (x, y, w), where x and y
        are the coordinates of the value and w is the weight of the value.
    res_x: resolution of the x axis
    res_y: resolution of the y axis
    spr: the amount of spread to the neighbouring pixels. if not specified, it is set to 0.25.
    range_x: the range of the x inputs (min, max) to include in the heatmap.
        If the x value is outside of this range, it is ignored. If not specified,
        the range is set to the min and max of the data
    range_y: the range of the y inputs (min, max) to include in the heatmap.
        If the y value is outside of this range, it is ignored. If not specified,
        the range is set to the min and max of the data

    return: a 2D list of values representing the heatmap
    """

    # if the range is not specified, it is set to the min and max of the data
    if range_x is None:
        range_x = (min(values, key=lambda x: x[0])[0], max(values, key=lambda x: x[0])[0])
    if range_y is None:
        range_y = (min(values, key=lambda x: x[1])[1], max(values, key=lambda x: x[1])[1])
    
    heatmap = [[0 for i in range(res_x)] for j in range(res_y)]
    offsets = [(0,0,1), (0,1,spr), (1,1,spr), (1,0,spr), (1,-1,spr), (0,-1,spr), (-1,-1,spr), (-1,0,spr), (-1,1,spr)]
    for x, y, w in values:
        if range_x[0] <= x <= range_x[1] and range_y[0] <= y <= range_y[1]:
            x = int((x - range_x[0]) / (range_x[1] - range_x[0]) * res_x)
            y = int((y - range_y[0]) / (range_y[1] - range_y[0]) * res_y)
            for offset in offsets:
                x2 = x + offset[0]
                y2 = y + offset[1]
                if 0 <= x2 < res_x and 0 <= y2 < res_y:
                    heatmap[y2][x2] += w*offset[2]
    return heatmap