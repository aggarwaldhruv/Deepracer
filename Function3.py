def reward_function(params):
	'''
	Example that penalizes slow driving. This create a non-linear reward function so it may take longer to learn.
	'''

	# Calculate 3 marks that are farther and father away from the center line
	marker_1 = 0.1 * params['track_width']
	marker_2 = 0.25 * params['track_width']
	marker_3 = 0.5 * params['track_width']

	# Give higher reward if the car is closer to center line and vice versa
	if params['distance_from_center'] <= marker_1:
		reward = 1
		reward = direction_function(params,reward)
	elif params['distance_from_center'] <= marker_2:
		reward = 0.5
		reward = direction_function(params,reward)
	elif params['distance_from_center'] <= marker_3:
		reward = 0.1
		reward = direction_function(params,reward)
	else:
		reward = 1e-3  # likely crashed/ close to off track

	# penalize reward for the car taking slow actions
	# speed is in m/s
	# the below assumes your action space has a maximum speed of 5 m/s and speed granularity of 3
	# we penalize any speed less than 2m/s
	SPEED_THRESHOLD = 2
	if params['speed'] < SPEED_THRESHOLD:
		reward *= 0.5

	return float(reward)
	
def direction_function(params , reward):
    import math
    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle
    speed = params['speed']

    SPEED_THRESHOLD = 4.5 
    
    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 30

	# Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

	# Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
	# Convert to degree
    track_direction = math.degrees(track_direction)

	# Cacluate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
	# Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 5.0
    
    if direction_diff < DIRECTION_THRESHOLD:
        reward = reward*1.4
    else:
        reward *= 0.6     
    return reward
