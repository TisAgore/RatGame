from collections import OrderedDict

deltas = [4, 2, 4, 2]
directions_for_deltas = ['top', 'bottom', 'left', 'right']
deltas_dict = OrderedDict()
for delta_id in range(len(deltas)):
    delta = deltas[delta_id]
    print(delta, deltas_dict, delta in deltas_dict)
    direction = directions_for_deltas[delta_id]
    if delta in deltas_dict:
        deltas_dict[delta] += [direction]
    else:
        deltas_dict[delta] = [direction]
print(deltas_dict)