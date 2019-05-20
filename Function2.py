def reward_function(params):
 '''
    In @params object:
    {
        "all_wheels_on_track": Boolean,    # flag to indicate if the vehicle is on the track
        "x": float,                        # vehicle's x-coordinate in meters
        "y": float,                        # vehicle's y-coordinate in meters
        "distance_from_center": float,     # distance in meters from the track center 
        "is_left_of_center": Boolean,      # Flag to indicate if the vehicle is on the left side to the track center or not. 
        "heading": float,                  # vehicle's yaw in degrees
        "progress": float,                 # percentage of track completed
        "steps": int,                      # number steps completed
        "speed": float,                    # vehicle's speed in meters per second (m/s)
        "streering_angle": float,          # vehicle's steering angle in degrees
        "track_width": float,              # width of the track
        "waypoints": [[float, float], … ], # list of [x,y] as milestones along the track center
        "closest_waypoints": [int, int]    # indices of the two nearest waypoints.
    }
    
    Speed : 5m/s
    Steering angle : 30
    Steering angle granularity : 5
    Speed granularity : 3
    
    HyperParameter Value{
        Gradient descent batch size :   128
        Entropy :   0.01
        Discount factor :	0.999
        Loss type   :	Huber
        Learning rate   :	0.0003
        Number of experience episodes between each policy-updating iteration    :	40
        Number of epochs    :	10
    }
    
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
	SPEED_THRESHOLD = 2.5
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
